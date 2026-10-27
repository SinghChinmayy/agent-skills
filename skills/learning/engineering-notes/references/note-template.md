# Note template

Copy this into `notes/<subject>/<topic>.md`. All front-matter fields are required except `aliases`.

Front matter is YAML: quote any value that contains `: ` (for example `summary: "Find candidates who have every skill: Python and SQL."`), or it will be misread and break the website build. `scripts/check_notes.py` catches this.

```markdown
---
title: Filtering grouped results with HAVING
subject: sql
summary: HAVING filters groups after aggregation; WHERE filters rows before it.
tags: [sql, aggregation, group-by]
status: learning          # learning | confident
created: 2026-10-03
updated: 2026-10-27
aliases: [having clause]  # optional: other names to search for
---

**In one line:** HAVING filters groups after they are aggregated; WHERE filters rows before they are grouped.

## How I think about it

The learner's own model, analogy or mnemonic, in their words.

## Explanation

Plain-language explanation in short sections. Define terms on first use.

## Example

A small, correct, runnable example, then what each important part does.

![Alt text that says what the diagram shows.](./assets/<topic>-<name>.svg)
*One-line caption.*

## Common mistakes

- Mistakes the learner made or is likely to make, and why they are wrong.

> **Correction:** In my notebook I wrote "…". That is not quite right: …

## Practice

- [001 · Data Science Skills](../../practice/sql/001-data-science-skills.md)

## Revision

### Key takeaways

- 3–5 one-line takeaways.

### Check yourself

<details>
<summary>Why can't an aggregate condition go in WHERE?</summary>

WHERE runs before rows are grouped, so the aggregate does not exist yet.

</details>

## History

- 2026-10-03: First notes, from notebook pages on GROUP BY.
- 2026-10-27: Added the "has all of these values" pattern.
```

## Practice file

`practice/<subject>/NNN-<slug>.md`:

```markdown
---
title: Data Science Skills
subject: sql
kind: practice
summary: Find candidates who have every required skill.
tags: [sql, having, count-distinct]
difficulty: easy          # easy | medium | hard
created: 2026-10-03
updated: 2026-10-03
related: [filtering-groups-with-having]
---

## Question
## My attempt        (optional; keep it even if wrong)
## Solution
## What this demonstrates
```
