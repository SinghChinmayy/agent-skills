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

1. **Record of understanding**: how *they* think about the topic, including the analogy that made it click.
2. **Revision sheet**: takeaways and self-check questions they can revise from in five minutes.
3. **Public showcase**: accurate, readable writing they are happy to publish.

Notes grow over time. A new notebook page about `JOIN`s extends the existing SQL joins note; it does not create `joins-2.md`.

## Repository layout (defaults)

The notes repository's `AGENTS.md` may override these paths. Read it first.

```text
inbox/                  drop zone, not committed except inbox/README.md
notes/<subject>/<topic>.md
notes/<subject>/assets/<topic>-<name>.svg
notes/<subject>/sources/<topic>-page-N.jpg   optional: kept notebook pages (see step 7)
practice/<subject>/NNN-<slug>.md    solved exercises and interview problems
log.md                  what was processed and where it went
scripts/check_notes.py  front-matter validator (run before committing)
```

`<subject>` is a short lowercase area such as `sql`, `networking`, `operating-systems`, `system-design`, `go`. `<topic>` is a kebab-case slug of the concept, not of the date or source.

## Workflow

### 1. Inventory the inbox

List every file in `inbox/` except `README.md`. Accept `.md`, `.txt`, images (`.jpg`, `.jpeg`, `.png`, `.heic`, `.webp`) and `.pdf`. Also collect any links the user gives with them (videos, articles, docs). Tell the user what you found in one short list before changing anything.

### 2. Read, and transcribe handwriting faithfully

- For images and PDFs, transcribe each page before interpreting it. Keep the learner's wording, abbreviations, arrows and margin comments. Describe hand-drawn sketches in words; they are evidence of how the learner pictures the idea.
- Mark anything you cannot read as `[?]`. If a `[?]` changes the meaning, ask the user about all of them in **one** message, quoting each unclear fragment. Never guess a technical term.
- Ignore personal content that is not study material (to-do items, phone numbers, names). It must never reach the notes.

### 3. Extract the essence

For each input, pull out:

- **Concepts** and the claims the learner makes about them.
- **Their understanding**: analogies, mnemonics, "the way I see it", diagrams they drew.
- **Examples**: code, queries, commands, worked numbers.
- **Doubts and weak spots**: questions they wrote, things they crossed out, and points they got wrong. These tell you what to explain more clearly and which general pitfalls to list. They are never shown as the learner's mistakes.
- **Practice**: exercises, interview questions, solved problems.
- **References**: videos, articles or docs the learner used or linked. Look up each one's real title and author (for a YouTube link, its oEmbed endpoint gives both) and list it under `## Further explanation`. Never describe what a video or page says unless you have actually read it or its transcript; cite it as further reading instead.

Check every technical claim. If the notebook is wrong, **fix it silently**: write the correct version as if it had always been right. Do not quote the mistake, add "Correction" callouts, or write "in my notebook I wrote…". The note is the clean, correct version; kept notebook pages, if any, are the record of what was originally written.

### 4. Place it: merge before you create

- Search existing notes (`notes/**/*.md`, by title, `tags` and headings) for the topic.
- **Existing topic**: merge the new material into the right section, extend examples, add new takeaways and questions, update `updated:`, and add one line to the note's `## History`. Preserve existing text; edit only what the new material changes.
- **New topic**: create `notes/<subject>/<topic>.md` from `references/note-template.md`.
- **Exercises** go to `practice/<subject>/NNN-<slug>.md` (next unused three-digit number), with the question, the learner's attempt if any, a correct solution, and "what this demonstrates". Link it from the related note's `## Practice`.
- If one input covers several topics, split it across their notes.
- Link notes and practice files to each other with relative `.md` paths (`../../practice/sql/001-….md`). They work on GitHub, and the website rewrites them to its own URLs.

### 5. Write in the learner's voice

- Write as the learner explaining it to their future self: first person where their notes are first person, plain language, short sections.
- Keep their analogies under **How I think about it**, even if informal, as long as they are not wrong.
- Define each term on first use. Prefer one small, correct example over three vague ones.
- **Algorithms and processes** (hashing, TCP handshakes, garbage collection, a sort) get a short numbered **How it works**: plain steps first, then detail. If the learner asked for "a simple algorithm", this is where it goes.
- **Run every code example** before committing, and paste its real output. If you add an implementation, test it against a trusted reference (a standard library, a known answer) on a few inputs, including edge cases. Code that has not run does not go in a note.
- Every note ends with the revision block: 3–5 **Key takeaways** and 3–5 **Check yourself** questions with answers inside `<details>`.

### 6. Diagrams: only when they earn their place

Add a diagram, or a small illustration, when the idea is about **order** (a pipeline, a request path, query evaluation), **structure** (trees, tables and keys, memory layout), **state** (transitions, lifecycles), or a **spatial comparison** (before and after). Do not add one for definitions, lists or anything a single sentence explains.

- At most two per note. Each needs alt text that states what it shows, plus a one-line caption.
- Use the sketch style in `references/diagram-style.md`: hand-drawn SVG, readable in light and dark mode. A small cute touch is welcome when it makes the idea memorable, never at the expense of accuracy.
- Save as `notes/<subject>/assets/<topic>-<name>.svg` and reference it relatively. Validate with `xmllint --noout` and look at a render before keeping it.

### 7. Keep pages, validate, log, tidy

1. **Keep the notebook pages, if the repository opts in.** Only when the notes repository's `AGENTS.md` says to keep notebook pages:
   1. Resize each photo to about 1500×2000 and compress it (`sips -Z 2000 -s formatOptions 72 in.jpg --out out.jpg` on macOS, or `magick in.jpg -resize 2000x2000 -quality 72 out.jpg`).
   2. Strip its metadata with `scripts/strip_metadata.py`. Phone photos can carry GPS coordinates and device details, and the pages are published.
   3. Save the result as `notes/<subject>/sources/<topic>-page-N.jpg`, and link the pages from the note under `## My notebook pages` in a `<details>` block, one image per page with a one-line caption.
   4. Never keep a page that shows personal content. Ask the user instead.
2. Run `python3 scripts/check_notes.py`. Fix every error.
3. Append to `log.md`: date, each input file, and the notes and practice files it changed.
4. Move processed inputs to `inbox/processed/<YYYY-MM-DD>/` (git-ignored), and keep them until the user has reviewed the result.
5. Update the subject index in the repository `README.md` if a note or practice file was added.

### 8. Commit; publish only on the user's word

Commit with `notes(<subject>): <what was learned>`, one commit per processed batch, on a branch named `notes-<topic>`. Show the user the list of changed notes and a two-line summary of each.

**Do not publish** until the user says so. Publishing means one of the routes the repository's `AGENTS.md` describes, usually:

- **Pull request** (preferred): push the branch and open a PR. If the repository auto-merges notes-only PRs, CI validates, merges and publishes it. Keep these PRs to notes content only (`notes/`, `practice/`, `log.md`, `README.md`). Put any change to scripts, workflows or `AGENTS.md` in a separate PR, because those wait for a human review.
- **Push to `main`**: CI validates and publishes directly.

After publishing, confirm it: the CI run passed, the website received the sync commit, and the note's page loads.

## Rules

- Never invent understanding the learner did not express. Your own explanations, examples and revision questions go in unmarked; analogies under "How I think about it" must be the learner's.
- Never showcase the learner's mistakes. Fix errors silently, and phrase pitfalls as general advice ("a common mistake is…"), never as "I got this wrong".
- Never publish raw notebook images. Publish processed pages (resized, metadata stripped) only when the repository opts in, and never pages with personal content.
- Never delete or rewrite an existing note wholesale. Edits are local and recorded in `## History`.
- Accuracy beats polish. When unsure about a fact, say so in the note or ask.
- One topic per file, one file per topic.
