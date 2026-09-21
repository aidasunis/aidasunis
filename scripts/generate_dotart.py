"""Converts an image into a stippled dot-matrix SVG, matching a
'point-cloud scan' aesthetic (bright pixel -> dot, dark background -> empty)."""
import sys
from PIL import Image

SRC = sys.argv[1]
OUT = sys.argv[2]
GRID_W = 90  # dots across
DOT_COLOR = "#A78BFA"
PANEL_SIZE = 340  # px, square panel to match the reference layout

img = Image.open(SRC).convert("L")  # grayscale
w, h = img.size
grid_h = round(GRID_W * h / w)
small = img.resize((GRID_W, grid_h), Image.LANCZOS)
pixels = small.load()

cell = PANEL_SIZE / GRID_W
threshold = 60  # brightness (0-255) below this = treated as background, no dot

dots = []
for y in range(grid_h):
    for x in range(GRID_W):
        b = pixels[x, y]
        if b < threshold:
            continue
        # brightness -> dot radius/opacity (brighter = bigger, more opaque)
        t = (b - threshold) / (255 - threshold)  # 0..1
        r = 0.55 + t * 1.15
        opacity = 0.35 + t * 0.65
        cx = x * cell + cell / 2
        cy = y * cell + cell / 2
        dots.append((cx, cy, r, opacity))

offset_y = (PANEL_SIZE - grid_h * cell) / 2

svg_dots = "\n".join(
    f'<circle cx="{cx:.2f}" cy="{cy + offset_y:.2f}" r="{r:.2f}" fill="{DOT_COLOR}" fill-opacity="{op:.2f}"/>'
    for cx, cy, r, op in dots
)

svg = f'''<svg width="{PANEL_SIZE}" height="{PANEL_SIZE}" viewBox="0 0 {PANEL_SIZE} {PANEL_SIZE}" xmlns="http://www.w3.org/2000/svg">
{svg_dots}
</svg>'''

with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)

print(f"dots: {len(dots)}  grid: {GRID_W}x{grid_h}")
