"""Hand-drawn style SVG diagrams for engineering notes.

Usage (from the notes repository):

    import sys; sys.path.insert(0, '<path to this skill>/scripts')
    from sketch import Sketch
    d = Sketch(800, 300, 'What the diagram shows, for screen readers.')
    d.box(30, 110, 120, 60, ['WHERE', 'filters rows'], 'blue')
    d.arrow([(154, 140), (196, 140)], label='then', lx=175, ly=130)
    d.bot(680, 150)            # optional mascot
    d.save('notes/sql/assets/having-order.svg')

Shapes get a subtle wobble filter; text never does, so it stays crisp.
Colours: red, green, blue, yellow, gray, purple, white.
"""

FONT = "'Comic Neue','Chalkboard SE','Comic Sans MS','Marker Felt',cursive"
INK, MUTED, RED = '#2b2b2b', '#5b6573', '#e5484d'
FILL = {'red': '#ffd6d7', 'green': '#d3f3e1', 'blue': '#dbe7ff', 'yellow': '#fff1c7',
        'gray': '#eef1f5', 'purple': '#ebe3fd', 'white': '#ffffff'}
EDGE = {'red': '#e5484d', 'green': '#30a46c', 'blue': '#276ef1', 'yellow': '#c99a1e',
        'gray': '#8a94a3', 'purple': '#7c5cd6', 'white': INK}


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


class Sketch:
    def __init__(self, w, h, label, seed=3):
        self.w, self.h, self.shapes, self.texts = w, h, [], []
        # The .s class sets fill:none, which beats fill="" attributes; colours
        # below are therefore always given through style="".
        self.head = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(label)}">
  <defs>
    <filter id="w" x="-5%" y="-5%" width="110%" height="110%">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="2" seed="{seed}"/>
      <feDisplacementMap in="SourceGraphic" scale="2.2"/>
    </filter>
    <marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker>
    <marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="{RED}"/></marker>
    <symbol id="bot" viewBox="0 0 80 110">
      <path d="M40 5 V16" class="s"/><circle cx="40" cy="5" r="4" style="fill:{RED}" class="s"/>
      <rect x="10" y="16" width="60" height="40" rx="11" style="fill:#dde3ea" class="s"/>
      <circle cx="28" cy="34" r="5" style="fill:{INK}"/><circle cx="52" cy="34" r="5" style="fill:{INK}"/>
      <path d="M31 45 Q40 52 49 45" class="s"/>
      <rect x="18" y="60" width="44" height="34" rx="8" style="fill:#c9d3df" class="s"/>
      <circle cx="40" cy="77" r="5" style="fill:#30a46c" class="s"/>
      <path d="M18 68 L6 82 M62 68 L74 82 M30 94 L30 106 M50 94 L50 106" class="s"/>
    </symbol>
    <style>
      text{{font-family:{FONT};fill:{INK}}}
      .mono{{font-family:'SF Mono',Menlo,Consolas,monospace}}
      .s{{stroke:{INK};stroke-width:2.2;fill:none;stroke-linecap:round;stroke-linejoin:round}}
    </style>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="#fffdf7"/>'''

    def box(self, x, y, w, h, lines, color='white', size=15, dashed=False, mono=False):
        """A rounded box; the first line is bold when there are several."""
        da = ' stroke-dasharray="7 6"' if dashed else ''
        self.shapes.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
                           f'style="fill:{FILL[color]};stroke:{EDGE[color]}" class="s"{da}/>')
        n, lh = len(lines), size * 1.3
        y0 = y + h / 2 - (n - 1) * lh / 2 + size * 0.35
        for i, t in enumerate(lines):
            bold = ' font-weight="700"' if i == 0 and n > 1 else ''
            cls = ' class="mono"' if mono and i > 0 else ''
            col = '' if i == 0 else f' style="fill:{MUTED}"'
            fs = size if i == 0 else size - 2
            self.texts.append(f'<text x="{x + w / 2}" y="{y0 + i * lh:.1f}" font-size="{fs}" '
                              f'text-anchor="middle"{bold}{cls}{col}>{esc(t)}</text>')

    def arrow(self, pts=None, curve=None, red=False, dashed=False, label=None, lx=0, ly=0):
        """A polyline through pts (or an SVG path in curve) with an arrowhead."""
        d = curve or 'M' + ' L'.join(f'{x} {y}' for x, y in pts)
        st = f' style="stroke:{RED}"' if red else ''
        da = ' stroke-dasharray="7 6"' if dashed else ''
        self.shapes.append(f'<path d="{d}" class="s"{st}{da} marker-end="url(#{"ar" if red else "a"})"/>')
        if label:
            self.text(lx, ly, label, 13, color=RED if red else MUTED)

    def text(self, x, y, t, size=15, anchor='middle', color=INK, bold=False, mono=False):
        fw = ' font-weight="700"' if bold else ''
        cls = ' class="mono"' if mono else ''
        self.texts.append(f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}"'
                          f'{fw}{cls} style="fill:{color}">{esc(t)}</text>')

    def bot(self, x, y, width=60):
        """The friendly robot mascot, top-left at (x, y). Use sparingly."""
        self.texts.append(f'<use href="#bot" x="{x}" y="{y}" width="{width}" height="{width * 1.375:.0f}"/>')

    def raw(self, svg, wobble=True):
        (self.shapes if wobble else self.texts).append(svg)

    def save(self, path):
        body = [self.head, '  <g filter="url(#w)">'] + ['    ' + s for s in self.shapes] + ['  </g>']
        body += ['  ' + t for t in self.texts] + ['</svg>\n']
        with open(path, 'w') as f:
            f.write('\n'.join(body))
