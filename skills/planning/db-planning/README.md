# db-planning

Talk the schema through first. Then write it down, versioned.

![A robot with a clipboard asks "Q 2.2: Does one user have many orders? Rec: yes, 1:N". An arrow leads to a whiteboard with users, orders, and items tables joined by one-to-many lines, then to a folder tree planning/db/v0 with stage-1.dbml, stage-1.md, stage-1.1.dbml, and stage-2.dbml](assets/db-planning.svg)

## What it does

Plans a database in two stages. First the agent interviews you, one question at a time with a recommended answer for each, until requirements are clear. Then it writes the design as a pair of files, a DBML schema you can paste into [dbdiagram.io](https://dbdiagram.io) and a Markdown plan, under `planning/db/`. Every later change becomes a new versioned file, so the design history is never overwritten. The agent talks in caveman mode throughout to keep the interview tight.

## When to use it

Say "plan db", "design database", "db planning", "database design", or "db design". Say "start" to get the first question straight away.

## How it works

![Stage 1: seven interview branches in order, purpose, entities, access, scale, rules, tech, ops. Once every branch is resolved or you say done, stage 2 writes v0/stage-1, then v0/stage-1.1 for a tweak, v0/stage-2 for a big shift, and v1/stage-1 in a new session, each as .dbml + .md](assets/db-planning-stages.svg)

**Stage 1, interview.** The agent walks a question tree depth-first: purpose and domain, entities and relationships, access patterns, scale and volume, constraints and rules (including GDPR, HIPAA, PCI, retention), tech and integrations, ops. Anything the codebase already answers gets looked up, not asked. It ends when every branch is resolved or you say "done", "enough", or "move on".

**Stage 2, plan files.** Each version is a `.dbml` and `.md` pair:

| Change | File | Example |
|--------|------|---------|
| First output | `v0/stage-1.*` | the first full snapshot |
| Small tweak (add a column, fix a relation) | `v0/stage-1.1.*`, `stage-1.2.*` | same direction, refined |
| Major shift (new entity, rethought access pattern) | `v0/stage-2.*` | sub-stage resets |
| New conversation | `v1/stage-1.*` | stage and sub-stage reset |

The `.dbml` holds tables with types, keys, indexes, notes, and `Ref` lines for every relationship. The `.md` covers summary, entities with row estimates (launch / 1 year / 5 years), key relationships, access patterns with index strategy, design decisions with reasons, open questions, and a change log.

## Install

Recommended: the open [`skills`](https://github.com/vercel-labs/skills) installer. Works with Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and most other agents, and asks which ones to install for. Run it from your project:

```bash
npx skills add SinghChinmayy/agent-skills --skill db-planning
```

Add `-g` to install it for all your projects. To skip the prompts and install straight into Claude Code:

```bash
npx skills add SinghChinmayy/agent-skills --skill db-planning -g -a claude-code -y
```

No Node? A skill is just a folder with a `SKILL.md`. For Claude Code:

```bash
mkdir -p ~/.claude/skills/db-planning && curl -fsSL https://raw.githubusercontent.com/SinghChinmayy/agent-skills/main/skills/planning/db-planning/SKILL.md -o ~/.claude/skills/db-planning/SKILL.md
```

For Codex and other agents that read `~/.agents/skills/`, swap the folder for `~/.agents/skills/db-planning`.

## Example

```text
You:   plan db
Agent: Q 1.1: Problem DB solves? Rec: car dealership inventory + sales.
You:   yes
Agent: Q 2.2: One user many orders? Rec: yes, 1:N, orders.user_id FK.
You:   yes, and an order has many items
...
You:   done
Agent: Wrote planning/db/v0/stage-1.dbml + stage-1.md.
```

```dbml
// Project: dealership · v0/stage-1 · 2026-10-26
Table users {
  id int [pk]
  email varchar [unique, not null]
}
Table orders {
  id int [pk]
  user_id int [not null, note: 'buyer']
  indexes { user_id }
}
Ref: orders.user_id > users.id
```

## Files

- [`SKILL.md`](./SKILL.md): full LLM-facing instructions
- [`assets/`](./assets/): the sketch and the stage diagram above
