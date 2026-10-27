# Diagram style

Hand-drawn, friendly, precise. Diagrams explain; the cute bits are seasoning.

## When to draw

| Draw it | Skip it |
| --- | --- |
| An order of steps (a pipeline, query evaluation order, request path) | A definition |
| A structure (tree, table relationships, memory layout, network topology) | A list of facts |
| States and transitions | Anything a code block already shows clearly |
| A before/after or side-by-side comparison | Decoration with no information |

## Look

- **Card**: an 800-wide `viewBox`, with a cream paper background `#fffdf7` in a rounded rect (`rx="18"`). The card keeps dark ink readable on the website's dark theme.
- **Ink**: strokes `#2b2b2b`, 2.2–2.5px, round caps and joins.
- **Wobble**: apply an `feTurbulence` + `feDisplacementMap` filter (scale about 2.4) to shapes only, never to text.
- **Palette** (fills): red `#ffd6d7`/`#e5484d`, green `#d3f3e1`/`#30a46c`, blue `#dbe7ff`/`#276ef1`, yellow `#fff1c7`/`#f5c451`, purple `#ebe3fd`, grey `#eef1f5`.
- **Text**: `'Comic Neue','Chalkboard SE','Comic Sans MS','Marker Felt',cursive`, at least 13px at 800 wide. Use `'SF Mono',Menlo,monospace` for code.
- **Optional mascot**: a small robot or stick figure, at most one per diagram and only if it carries a label or a point.

## Gotchas

- A CSS class with `fill:none` beats a `fill=""` attribute. Give filled shapes `style="fill:#…"` (the same goes for `stroke`).
- Always set `role="img"` and an `aria-label` that states what the diagram shows.
- Keep files under about 15 KB, and do not embed raster images.
- Validate with `xmllint --noout file.svg`, then render it (for example, headless Chrome `--screenshot`) and look for clipped text and lines running through boxes.

## Helper

`scripts/sketch.py` draws boxes, arrows and labels in this style:

```python
from sketch import Sketch
d = Sketch(800, 300, 'Query evaluation order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY.')
d.box(30, 110, 110, 60, ['FROM', 'pick rows'], 'gray')
d.arrow([(144, 140), (176, 140)])
d.save('notes/sql/assets/having-order.svg')
```
