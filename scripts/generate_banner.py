"""Generates the full two-panel terminal banner: VISUAL.MAP (dot-art) + SYSTEM.INFO."""
import sys
from PIL import Image

SRC = sys.argv[1]
OUT = sys.argv[2]

# ---- palette ----
BG_TOP = "#1a1625"
BG_BOTTOM = "#100e1a"
BORDER = "#A78BFA"
ACCENT = "#A78BFA"
ACCENT2 = "#7DD3FC"
TEXT = "#e9e6f2"
DIM = "#8b8398"
MONO = "'JetBrains Mono','Fira Code',Consolas,monospace"

# ---- layout ----
PAD = 20
CHROME_H = 42
BOX = 300  # square dot-art box
GAP = 26
LEFT_W = BOX
RIGHT_W = 420
CONTENT_W = LEFT_W + GAP + RIGHT_W
W = CONTENT_W + PAD * 2
COL_TOP = CHROME_H + 34
LABEL_H = 24
STATUS_H = 36
H = COL_TOP + LABEL_H + BOX + 30 + STATUS_H + PAD

# ---- dot art ----
GRID_W = 90
img = Image.open(SRC).convert("L")
iw, ih = img.size
grid_h = round(GRID_W * ih / iw)
small = img.resize((GRID_W, grid_h), Image.LANCZOS)
pixels = small.load()
cell = BOX / GRID_W
threshold = 60

dots = []
for y in range(grid_h):
    for x in range(GRID_W):
        b = pixels[x, y]
        if b < threshold:
            continue
        t = (b - threshold) / (255 - threshold)
        r = 0.5 + t * 1.05
        op = 0.35 + t * 0.65
        cx = x * cell + cell / 2
        cy = y * cell + cell / 2
        dots.append((cx, cy, r, op))
offset_y = (BOX - grid_h * cell) / 2

left_x = PAD
right_x = PAD + LEFT_W + GAP
box_y = COL_TOP + LABEL_H

dot_svg = "\n    ".join(
    f'<circle cx="{cx:.2f}" cy="{cy + offset_y:.2f}" r="{r:.2f}" fill="{ACCENT}" fill-opacity="{op:.2f}"/>'
    for cx, cy, r, op in dots
)

# corner brackets for the visual map box
bl = 14  # bracket arm length


def corner(cx, cy, dx, dy):
    return f'<path d="M{cx} {cy+dy*bl} V{cy} H{cx+dx*bl}" stroke="{ACCENT}" stroke-opacity="0.5" stroke-width="1.5" fill="none"/>'


brackets = "\n    ".join([
    corner(left_x, box_y, 1, 1),
    corner(left_x + BOX, box_y, -1, 1),
    corner(left_x, box_y + BOX, 1, -1),
    corner(left_x + BOX, box_y + BOX, -1, -1),
])

# ---- system.info rows ----
rows = [
    ("Subject", "Aida"),
    ("Role", "Mechatronics Engineering Student"),
    ("Focus", "Software · Apps · Web"),
    ("Off-duty", "Photography · Nature · Drawing"),
    ("Status", "Building + Learning + Shipping"),
    ("Core.Frontend", "React · Tailwind · JavaScript"),
    ("Core.Basics", "HTML · CSS"),
    ("ToolChain", "Git · GitHub · VS Code"),
    ("Explores", "Productivity apps"),
    ("Grid.GitHub", "aidasunis"),
    ("Grid.Instagram", "aidapsunis"),
]
row_h = BOX / (len(rows) - 1) if len(rows) > 1 else BOX
row_h = min(row_h, 34)
rows_svg_parts = []
ry = box_y + 6
for label, value in rows:
    rows_svg_parts.append(
        f'<text x="{right_x}" y="{ry:.1f}" font-family="{MONO}" font-size="13.5" fill="{DIM}">{label}</text>'
        f'<text x="{right_x + RIGHT_W}" y="{ry:.1f}" font-family="{MONO}" font-size="13.5" fill="{TEXT}" text-anchor="end">{value}</text>'
    )
    ry += row_h
rows_svg = "\n    ".join(rows_svg_parts)

status_y = box_y + BOX + STATUS_H

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG_TOP}"/>
      <stop offset="100%" stop-color="{BG_BOTTOM}"/>
    </linearGradient>
  </defs>

  <rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
  <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="13.5" fill="none" stroke="{BORDER}" stroke-opacity="0.35" stroke-width="1.5"/>

  <!-- terminal chrome -->
  <path d="M0.75 14A13.25 13.25 0 0 1 14 0.75h{W-28}A13.25 13.25 0 0 1 {W-0.75} 14v28H0.75V14Z" fill="#1f1b2e"/>
  <line x1="0.75" y1="{CHROME_H}" x2="{W-0.75}" y2="{CHROME_H}" stroke="{BORDER}" stroke-opacity="0.2" stroke-width="1"/>
  <circle cx="27" cy="21" r="6" fill="#FF5F57"/>
  <circle cx="47" cy="21" r="6" fill="#FEBC2E"/>
  <circle cx="67" cy="21" r="6" fill="#28C840"/>
  <text x="{W/2}" y="25.5" font-family="{MONO}" font-size="13" fill="{DIM}" text-anchor="middle">profile.sh --live</text>

  <!-- left column label -->
  <text x="{left_x}" y="{COL_TOP+16}" font-family="{MONO}" font-size="13" font-weight="700" fill="{ACCENT2}">VISUAL.MAP</text>
  <text x="{left_x+BOX}" y="{COL_TOP+16}" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="end">{GRID_W}x{grid_h} / 1-BIT</text>

  <!-- dot art -->
  <g transform="translate({left_x},{box_y})">
    {dot_svg}
  </g>
  {brackets}
  <text x="{left_x}" y="{box_y+BOX+20}" font-family="{MONO}" font-size="11" fill="{DIM}">PTS {len(dots)} · FS/SERPENTINE</text>

  <!-- right column label -->
  <text x="{right_x}" y="{COL_TOP+16}" font-family="{MONO}" font-size="13" font-weight="700" fill="{ACCENT2}">SYSTEM.INFO</text>
  <circle cx="{right_x+RIGHT_W-148}" cy="{COL_TOP+12}" r="3.5" fill="#f87171"/>
  <text x="{right_x+RIGHT_W-140}" y="{COL_TOP+16}" font-family="{MONO}" font-size="11" font-weight="700" fill="#f87171">LIVE</text>
  <rect x="{right_x+RIGHT_W-100}" y="{COL_TOP+2}" width="100" height="18" rx="9" fill="#2a2440" stroke="{BORDER}" stroke-opacity="0.4"/>
  <text x="{right_x+RIGHT_W-50}" y="{COL_TOP+14.5}" font-family="{MONO}" font-size="10.5" fill="{TEXT}" text-anchor="middle">@aidasunis</text>

  <!-- info rows -->
  {rows_svg}

  <!-- status bar -->
  <line x1="{PAD}" y1="{status_y-10}" x2="{W-PAD}" y2="{status_y-10}" stroke="{BORDER}" stroke-opacity="0.15" stroke-width="1"/>
  <circle cx="{PAD+4}" cy="{status_y+8}" r="3" fill="#4ade80"/>
  <text x="{PAD+14}" y="{status_y+12}" font-family="{MONO}" font-size="11" fill="{DIM}">ALL SYSTEMS NOMINAL</text>
  <text x="{W-PAD}" y="{status_y+12}" font-family="{MONO}" font-size="11" fill="{DIM}" text-anchor="end">UTC-5 · LATAM NODE</text>
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"dots: {len(dots)}  size: {W}x{H}")
