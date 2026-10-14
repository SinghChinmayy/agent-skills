---
name: og-generator
description: Skill to generate Open Graph images for Catalyst Bridge using headless Chrome.
---

# Overview
This skill encapsulates the entire OG‑image generation pipeline that was previously stored in `scripts/og/`. It provides a reusable command that can be invoked from the Antigravity CLI or other automation.

## Files
- `template-a.html` – Layout with logo top‑left.
- `template-b.html` – Layout with centered logo.
- `generate-og.sh` – Shell script that renders both templates with headless Chrome, creates 1200 × 630 px PNGs and 300 px previews, and validates dimensions.

## Usage
```sh
agy run og-generator generate
```
The skill will place the resulting PNGs in `scripts/tmp/og/` (same as before) and optionally copy the chosen variant to `public/og-image.png`.

## Design compliance
- Uses the Sora font via `@font-face` referencing the read‑only resources folder.
- Logo width 240 px respects the clear‑space rule from `DESIGN.md`.
- Headline 84 px, domain 28 px – matches the visual prominence requirements.
- Colors and contrast are verified against `DESIGN.md` (Ivory on Harbour Navy, 14.73:1).

## Extensibility
Run the script with `VARIANT=A` or `VARIANT=B` to generate a specific layout, or modify the templates inside this skill for future branding updates.
