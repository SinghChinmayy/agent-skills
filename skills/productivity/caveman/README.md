# caveman

Talk like smart caveman. Same brain, fewer tokens.

![A verbose robot with a giant bubble of filler words next to a caveman robot with a club saying "Bug in auth. < not <=. Fix:", while a bar chart drops from 312 tokens to 78](assets/caveman.svg)

## What it does

Compress every model response to caveman-style prose. Drops articles, filler, pleasantries, and hedging. Keeps every technical detail, code block, error string, and symbol exact. Cuts ~65-75% of output tokens with full accuracy preserved. Mode persists for the whole session until changed or stopped.

Six intensity levels:

| Level | What change |
|-------|-------------|
| `lite` | Drop filler/hedging. Sentences stay full. Professional but tight. |
| `full` | Default. Drop articles, fragments OK, short synonyms. |
| `ultra` | Bare fragments. Abbreviations (DB, auth, fn). Arrows for causality. |
| `wenyan-lite` | Classical Chinese register, light compression. |
| `wenyan-full` | Maximum 文言文. 80-90% character reduction. |
| `wenyan-ultra` | Extreme classical compression. |

What never gets squashed: code blocks, function and API names, error strings (quoted exactly), and commits or PRs, which stay in normal prose.

## When to use it

Say "caveman mode", "talk like caveman", "use caveman", "less tokens", or "be brief", or invoke `/caveman`. It also kicks in when you ask for token efficiency.

```
/caveman              # full mode (default)
/caveman lite         # lighter compression
/caveman ultra        # extreme compression
/caveman wenyan       # classical Chinese
stop caveman          # back to normal prose ("normal mode" works too)
```

## How it works

Every answer follows one pattern:

```
[thing] [action] [reason]. [next step].
```

1. **Drop** articles, filler (just, really, basically), pleasantries (sure, happy to), and hedging.
2. **Keep** technical terms, code, symbols, and error strings exactly as they are.
3. **Persist** on every response in the session. No drifting back to chatty after a few turns.
4. **Auto-clarity**: drop to normal prose for security warnings, irreversible-action confirmations, multi-step sequences where fragment ambiguity risks misread, and when you repeat a question. Resume caveman after the clear part.

> **Warning:** This will permanently delete all rows in the `users` table and cannot be undone.
> ```sql
> DROP TABLE users;
> ```
> Caveman resume. Verify backup exist first.

## Install

Recommended: the open [`skills`](https://github.com/vercel-labs/skills) installer. Works with Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI and most other agents, and asks which ones to install for. Run it from your project:

```bash
npx skills add SinghChinmayy/agent-skills --skill caveman
```

Add `-g` to install it for all your projects. To skip the prompts and install straight into Claude Code:

```bash
npx skills add SinghChinmayy/agent-skills --skill caveman -g -a claude-code -y
```

No Node? A skill is just a folder with a `SKILL.md`. For Claude Code:

```bash
mkdir -p ~/.claude/skills/caveman && curl -fsSL https://raw.githubusercontent.com/SinghChinmayy/agent-skills/main/skills/productivity/caveman/SKILL.md -o ~/.claude/skills/caveman/SKILL.md
```

For Codex and other agents that read `~/.agents/skills/`, swap the folder for `~/.agents/skills/caveman`.

## Example

Question: "Why does my React component re-render?"

Normal prose:
> Your component re-renders because you create a new object reference each render. Wrapping it in `useMemo` will fix the issue.

Caveman (full):
> New object ref each render. Inline object prop = new ref = re-render. Wrap in `useMemo`.

Caveman (ultra):
> Inline obj prop → new ref → re-render. `useMemo`.

## Files

- [`SKILL.md`](./SKILL.md): full LLM-facing instructions
- [`assets/caveman.svg`](./assets/caveman.svg): the sketch above
