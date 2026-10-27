---
name: engineering-notes
description: >
  Turns raw study material (Markdown notes, photos or PDFs of handwritten notebook
  pages) dropped in an inbox into continuous, topic-wise engineering notes that keep
  the learner's own understanding, add revision questions, and include a diagram only
  when it genuinely helps. Notes live in a notes repository and are published to a
  website by CI. Triggers on: "process my notes", "process the inbox", "digest my
  notes", "add this to my notes", "engineering notes", "write up what I learned".
---

# Engineering notes from a notebook

## Goal

Capture the essence of what the learner studied, in their own understanding, as one growing note per topic. Each note has to work three ways:

1. **Record of understanding**: how *they* think about the topic, including the analogy that made it click and the mistake they used to make.
2. **Revision sheet**: takeaways and self-check questions they can revise from in five minutes.
3. **Public showcase**: accurate, readable writing they are happy to publish.

Notes grow over time. A new notebook page about `JOIN`s extends the existing SQL joins note; it does not create `joins-2.md`.

## Repository layout (defaults)

The notes repository's `AGENTS.md` may override these paths. Read it first.

```text
inbox/                  drop zone, not committed except inbox/README.md
notes/<subject>/<topic>.md
notes/<subject>/assets/<topic>-<name>.svg
practice/<subject>/NNN-<slug>.md    solved exercises and interview problems
log.md                  what was processed and where it went
scripts/check_notes.py  front-matter validator (run before committing)
```

`<subject>` is a short lowercase area such as `sql`, `networking`, `operating-systems`, `system-design`, `go`. `<topic>` is a kebab-case slug of the concept, not of the date or source.

## Workflow

### 1. Inventory the inbox

List every file in `inbox/` except `README.md`. Accept `.md`, `.txt`, images (`.jpg`, `.jpeg`, `.png`, `.heic`, `.webp`) and `.pdf`. Tell the user what you found in one short list before changing anything.

### 2. Read, and transcribe handwriting faithfully

- For images and PDFs, transcribe each page before interpreting it. Keep the learner's wording, abbreviations, arrows and margin comments. Describe hand-drawn sketches in words; they are evidence of how the learner pictures the idea.
- Mark anything you cannot read as `[?]`. If a `[?]` changes the meaning, ask the user about all of them in **one** message, quoting each unclear fragment. Never guess a technical term.
- Ignore personal content that is not study material (to-do items, phone numbers, names). It must never reach the notes.

### 3. Extract the essence

For each input, pull out:

- **Concepts** and the claims the learner makes about them.
- **Their understanding**: analogies, mnemonics, "the way I see it", diagrams they drew.
- **Examples**: code, queries, commands, worked numbers.
- **Mistakes and doubts**: things they got wrong, crossed out, or wrote as questions.
- **Practice**: exercises, interview questions, solved problems.

Check every technical claim. If the notebook is wrong, keep what they wrote and add a visible correction (see the template). A visible correction is more useful for revision, and more honest, than a silent rewrite.

### 4. Place it: merge before you create

- Search existing notes (`notes/**/*.md`, by title, `tags` and headings) for the topic.
- **Existing topic**: merge the new material into the right section, extend examples, add new takeaways and questions, update `updated:`, and add one line to the note's `## History`. Preserve existing text; edit only what the new material changes.
- **New topic**: create `notes/<subject>/<topic>.md` from `references/note-template.md`.
- **Exercises** go to `practice/<subject>/NNN-<slug>.md` (next unused three-digit number), with the question, the learner's attempt if any, a correct solution, and "what this demonstrates". Link it from the related note's `## Practice`.
- If one input covers several topics, split it across their notes.

### 5. Write in the learner's voice

- Write as the learner explaining it to their future self: first person where their notes are first person, plain language, short sections.
- Keep their analogies under **How I think about it**, even if informal, as long as they are not wrong.
- Define each term on first use. Prefer one small, correct example over three vague ones.
- Every note ends with the revision block: 3–5 **Key takeaways** and 3–5 **Check yourself** questions with answers inside `<details>`.

### 6. Diagrams: only when they earn their place

Add a diagram when the idea is about **order** (a pipeline, a request path, query evaluation), **structure** (trees, tables and keys, memory layout), **state** (transitions, lifecycles), or a **spatial comparison** (before and after). Do not add one for definitions, lists or anything a single sentence explains.

- At most two per note. Each needs alt text that states what it shows, plus a one-line caption.
- Use the sketch style in `references/diagram-style.md`: hand-drawn SVG, readable in light and dark mode. A small cute touch is welcome when it makes the idea memorable, never at the expense of accuracy.
- Save as `notes/<subject>/assets/<topic>-<name>.svg` and reference it relatively. Validate with `xmllint --noout` and look at a render before keeping it.

### 7. Validate, log, tidy

1. Run `python3 scripts/check_notes.py`. Fix every error.
2. Append to `log.md`: date, each input file, and the notes and practice files it changed.
3. Move processed inputs to `inbox/processed/<YYYY-MM-DD>/` (git-ignored), and keep them until the user has reviewed the result.
4. Update the subject index in the repository `README.md` if a note or practice file was added.

### 8. Commit; publish only on the user's word

Commit with `notes(<subject>): <what was learned>`, one commit per processed batch. Show the user the list of changed notes and a two-line summary of each. **Do not push** until the user says so: pushing to `main` publishes to the website through CI.

## Rules

- Never invent understanding the learner did not express. Mark your additions so they can be told apart (`> **Added:**` callouts or the Correction format).
- Never publish raw notebook images or personal content.
- Never delete or rewrite an existing note wholesale. Edits are local and recorded in `## History`.
- Accuracy beats polish. When unsure about a fact, say so in the note or ask.
- One topic per file, one file per topic.
