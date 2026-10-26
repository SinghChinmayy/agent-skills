---
name: modular-development
description: >
  Scoped, test-driven development workflow. AI edits ONLY the isolated module/files
  explicitly listed in the current phase. Prevents codebase contamination by enforcing
  a build → test → review → merge → global-check pipeline.
  Trigger: "modular dev", "modular mode", "/modular", "scoped build", "isolated module".
---

# Modular Development Skill

A disciplined, phase-gated workflow for building, testing, and integrating isolated logic without touching unrelated parts of the codebase.

---

## Core Principle

> **AI scope is LOCKED to the active phase files.** No edits outside declared scope until developer explicitly unlocks the next phase.

---

## Workflow Phases

### Phase 1 — SCOPE DECLARATION
**Who:** Developer  
**What:** Define the module/feature boundary before any code is written.

Developer must declare:
```
MODULE:   <name>
FILES IN SCOPE: <exhaustive list of files/dirs AI may touch>
GOAL:     <one-sentence description of what this module does>
ENTRY:    <function / API / component name being built>
```

AI must echo back the scope and ask for confirmation before writing any code.  
**AI MUST NOT edit any file not in `FILES IN SCOPE`.**

---

### Phase 2 — ISOLATED BUILD
**Who:** AI (scope-locked)  
**What:** Implement only the declared logic inside the declared files.

Rules:
- Write code only in `FILES IN SCOPE`.
- No importing/modifying external modules unless they are read-only (no edits).
- If a missing dependency is discovered, STOP and report to developer — do not create new files outside scope silently.
- Keep public API surface minimal; expose only what the integration will need.
- Add inline comments explaining non-obvious decisions.

Output: working isolated module with clearly defined exports/interfaces.

---

### Phase 3 — MODULE TESTS
**Who:** AI (scope-locked to module + its test file)  
**What:** Write unit/integration tests covering the module in isolation.

Rules:
- Test file lives adjacent to or in a `/tests` subfolder matching the module path.
- Mock ALL external dependencies — tests must not require the rest of the codebase to run.
- Cover: happy path, edge cases, error/failure cases.
- Tests must be runnable with a single command (document it).
- Minimum coverage targets (adjust per project): **80% lines, 100% exported functions**.

Output: test file + command to run tests + passing test results (paste output).

---

### Phase 4 — DEVELOPER REVIEW GATE ⛔
**Who:** Developer  
**What:** Review module code + tests before any merge.

AI presents:
1. Summary of what was built (3–5 bullets).
2. Files changed (diff summary or list).
3. Test results output.
4. Any TODOs / known limitations.
5. Proposed integration point (where/how it plugs into codebase).

**AI WAITS.** No further action until developer gives one of:
- `approve` → proceed to Phase 5
- `revise: <feedback>` → AI reworks within scope, loops back to Phase 3
- `abort` → discard module work

---

### Phase 5 — CONTROLLED MERGE
**Who:** AI (scope expands to integration files ONLY)  
**What:** Wire the module into the existing codebase at the single declared integration point.

Rules:
- Developer must explicitly list the **integration files** (e.g., router, index, service registry).
- AI edits ONLY those integration files + the module files.
- Changes are additive — no refactoring of pre-existing logic in integration files.
- If a conflict or unexpected dependency is found, STOP and report before touching anything.

Output: integration diff (files changed + what was added).

---

### Phase 6 — GLOBAL TEST CHECK
**Who:** AI  
**What:** Run the full project test suite and reconcile new tests.

Steps:
1. Run existing global test suite. Paste output.
2. Identify any broken pre-existing tests caused by integration.
3. Fix ONLY breakage directly caused by the new module (no opportunistic refactors).
4. Add the new module's tests to the global suite if not auto-discovered.
5. Run suite again — must be fully green before declaring done.

Output: before/after test output, list of fixes made.

---

## Scope Guard Rules (always enforced)

| Situation | AI Action |
|-----------|-----------|
| File outside scope needs edit | STOP. Report to dev. Ask to expand scope explicitly. |
| Discovered bug in unrelated code | Note it. Do NOT fix. File a separate task. |
| Tempted to "clean up" nearby code | Do NOT. Out of scope. |
| Test reveals need for new shared util | STOP. Propose util in Phase 4 review. Dev decides. |
| Integration causes unrelated breakage | STOP. Report root cause. Do NOT fix unrelated code. |

---

## Commands

| Command | Effect |
|---------|--------|
| `/modular start` | Begin Phase 1 — AI prompts for scope declaration |
| `/modular scope` | AI echoes current scope lock |
| `/modular status` | AI shows current phase + next required action |
| `/modular expand <files>` | Developer adds files to scope mid-session |
| `/modular approve` | Advance past current gate (Phase 4 or Phase 6) |
| `/modular revise <feedback>` | Loop back within current phase with feedback |
| `/modular abort` | Discard current module work, reset scope |
| `/modular done` | Close out — AI writes brief completion summary |

---

## Phase Status Template

When `/modular status` is called, output:

```
MODULAR DEV STATUS
==================
Module:   <name>
Phase:    <1-6 / name>
Scope:    <files locked>
Pending:  <what needs to happen next>
Gate:     <OPEN | WAITING FOR DEV | PASSED>
```

---

## Anti-Patterns (AI must refuse these)

- Refactoring code outside the declared module during Phase 2.
- Skipping Phase 3 tests because "it's simple".
- Auto-merging without explicit `approve` in Phase 4.
- Fixing discovered bugs in other modules "while I'm in there".
- Adding dependencies to `package.json` / `requirements.txt` without reporting.

---

## Activation

When triggered, AI must:
1. Announce: `Modular Development mode active. Scope is LOCKED until you declare files.`
2. Prompt developer for the Phase 1 scope declaration.
3. Echo confirmed scope back before writing any code.
