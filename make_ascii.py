"""Convert portrait to ASCII (ascii.txt) with background removed."""
import numpy as np
from PIL import Image, ImageOps, ImageFilter

SRC = "/mnt/user-data/uploads/file_00000000d310820ba689e5e384301a40.png"
COLS = 80
ASPECT = 0.5          # char height/width compensation (SVG uses 6x12 cells)
RAMP = " .:-=+*#%@"   # dark -> dense (dense = bright on dark theme)

raw = Image.open(SRC).convert("RGBA")
flat = Image.new("RGBA", raw.size, (255,255,255,255)); flat.alpha_composite(raw)
im = flat.convert("RGB")
alpha = raw.split()[3]
w, h = im.size
# crop: head + a bit of collar
box=(170, 140, 910, 1130)
im = im.crop(box); alpha = alpha.crop(box)
g = np.asarray(im.convert("L"), dtype=float)
rgb = np.asarray(im, dtype=float)

# background mask: near-white
bgim = alpha.point(lambda v: 255 if v < 128 else 0).filter(ImageFilter.MedianFilter(5))

cw, ch = im.size
rows = int(COLS * (ch / cw) * ASPECT)
gl = im.convert("L")
blur = gl.filter(ImageFilter.GaussianBlur(40))
loc = np.asarray(gl, dtype=float) - np.asarray(blur, dtype=float)
mix = np.asarray(gl, dtype=float) * 0.55 + (128 + loc * 2.6) * 0.45
small = Image.fromarray(np.clip(mix, 0, 255).astype(np.uint8)).resize((COLS, rows), Image.LANCZOS)
mask = np.asarray(alpha.resize((COLS, rows), Image.BOX), dtype=float) < 235
a = np.asarray(small, dtype=float)

fg = a[~mask]
lo, hi = np.percentile(fg, 2), np.percentile(fg, 98)
a = np.clip((a - lo) / (hi - lo), 0, 1)
# local contrast boost via equalization on foreground
vals = np.sort(a[~mask]); 
eq = np.searchsorted(vals, a) / len(vals)
a = np.where(mask, 0, 0.12 + 0.88 * np.clip(eq, 0, 1) ** 1.1)

lines = []
for y in range(rows):
    s = "".join(" " if mask[y, x] else RAMP[1 + min(len(RAMP)-2, int(a[y, x] * (len(RAMP)-1)))] for x in range(COLS))
    lines.append(s.rstrip())
open("ascii.txt", "w").write("\n".join(lines))
print("\n".join(lines))
