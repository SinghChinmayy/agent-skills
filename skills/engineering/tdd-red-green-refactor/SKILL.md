---
name: tdd-red-green-refactor
description: >
  Test-driven development workflow for any language or framework. Builds one behavior
  at a time with separate red, green, and optional refactor commits so git history
  proves tests came before code. Use for feature or bug-fix implementation.
  Triggers on: "tdd", "red green refactor", "test first", "write the test first",
  "implement with tests".
---

# TDD red-green-refactor workflow

Build one small behavior at a time. Each phase is its own commit so the git history proves tests came before code.

## The cycle

1. **Red**: write ONE failing test for one behavior. Run it and confirm it fails for the intended reason (an assertion, not an import error, missing module, or typo). Commit as `test: <behavior> (red)`. Touch only tests, plus minimal stubs if needed so the test can import or compile.
2. **Green**: write the minimum code that makes that test pass. Nothing extra. Commit as `feat: <behavior>` (or `fix: <behavior>`). Put any migration or schema change the code needs in this commit, not in the red.
3. **Refactor** (optional): improve structure with behavior unchanged and the full suite green. Commit as `refactor: <what>`. Skip it if there is nothing worth cleaning.

## Rules

- One behavior per cycle. Never add many failing tests in one commit.
- A new test that passes immediately is not red. It is redundant or wrong; fix or drop it (or see guard tests below).
- Run the full suite before every green and refactor commit, not just the new test.
- Never squash, reorder, or rewrite history. The honest trail is the deliverable.
- Foundations (config, DB connection, test fixtures, error format, tooling) are committed as `chore:`, not TDD cycles.

## Plan the slice first

Before writing code, list the behaviors the feature needs as one-line test names. Then order them:

1. **Foundations**: config, persistence setup, test fixtures, shared error format (`chore:`).
2. **Core domain rules**: the happy path of each business rule.
3. **Edge cases and errors**: validation, not-found, conflicts, permissions.
4. **Integration / UI**: start a UI screen only after the API it calls is green. Component tests follow the same red/green commits.
5. **End-to-end last**: few journeys, only after the pieces underneath are green.

Work the list top to bottom, one cycle per item. Add new items to the list as they surface instead of widening the current cycle.

## Test tooling (discover, don't assume)

- Find the project's test runner and coverage command before the first cycle: check `package.json` scripts, `pyproject.toml` / `setup.cfg` / `tox.ini`, `Makefile`, `go.mod`, `Cargo.toml`, `pom.xml` / `build.gradle`, CI workflow files, and the README.
- Use the project's existing test layout, naming, and fixtures. Do not add a new framework without asking.
- For persistence logic, prefer real dependencies (e.g. a real database via containers or a local test instance) over mocks. Mock only true external boundaries (third-party APIs, clocks, email).
- If no runner exists yet, set it up as a `chore:` commit before the first red.

## Guard tests

Some rules cannot honestly start red because the framework already enforces them (e.g. schema validation rejects a missing field). Do not fake a red. Commit the test as `test: <rule>` without the `(red)` suffix, and say in the body that it guards existing behavior and why it passed on first run.

## Race conditions: prove it honestly

For any shared-state write (stock counts, balances, seat bookings, unique claims):

1. **Red**: a test fires N concurrent actors at a limited resource (e.g. 20 buyers, 5 units) and asserts exact outcomes: 5 successes, 15 rejections, final count 0.
2. **Green (naive)**: read, modify, write. Run the test and watch it fail (oversell or lost update). Commit it as the naive attempt so the failure is on record.
3. **Fix**: make the write atomic (conditional update such as `UPDATE ... SET n = n - 1 WHERE id = ? AND n > 0`, row lock, optimistic version check, or unique constraint), with related writes in the same transaction. Test passes; commit as `fix:`.

Give each actor its own connection/session and a pool larger than N, or the test serializes and proves nothing.

## Merge policy

Merge with rebase or a merge commit only. Never squash-merge a TDD branch: squashing deletes the red-before-green history the workflow exists to produce.

## AI co-authorship

Every commit where an AI tool helped (including red commits with AI-written tests) ends with two blank lines, then a `Co-authored-by:` trailer using the tool's real address:

- Claude: `Co-authored-by: Claude <noreply@anthropic.com>`
- Codex: `Co-authored-by: OpenAI Codex <codex@users.noreply.github.com>`

Never invent a `<name>@users.noreply.github.com` address; GitHub credits whichever real account owns that username. Add a short body line saying what the AI did and what was done manually.

Optional, only if the project's AGENTS.md / CLAUDE.md asks for it:

- Keep raw, unedited AI chat logs (or public chat links) in a root `PROMPTS.md`. No summaries.
- Maintain a "My AI Usage" README section: tools used, how, and a reflection. Append; never remove earlier entries.

## Before finishing

- Run the full suite with coverage using the project's command and report the result.
- Note any assumptions or choices the spec left open (in the PR description or README, per project convention).

## Commit message examples

```text
chore: add test database fixture

test: registering a duplicate email returns 409 (red)

feat: return 409 on duplicate email

refactor: extract email normalization helper

test: missing email is rejected with 422

Guard test: request validation already rejects this, so it passed
on first run. Kept to pin the behavior.


Co-authored-by: Claude <noreply@anthropic.com>
```
