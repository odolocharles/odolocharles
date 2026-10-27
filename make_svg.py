"""Build a fastfetch-style SVG: ASCII art (ascii.txt) on the left, info on the right."""
import html

art = open("ascii.txt", encoding="utf-8").read().splitlines()

info = [
    ("title", "charles@sorabbyngo"),
    ("rule",  "─" * 44),
    ("Role",      "Founder & CEO"),
    ("Companies", "Sorabbyngo Inc, T13 Systems, Varlenyx"),
    ("Focus",     "AI research, systems engineering"),
    ("Email",     "odolocharles@gmail.com"),
    ("Phone",     "+254 112 413 670"),
    ("GitHub",    "github.com/odolocharles"),
    ("blank", ""),
    ("AI",      "PyTorch, TensorFlow, LLMs, RAG, Agents"),
    ("Systems", "Linux, Distributed Systems, Backend"),
    ("Web3",    "Smart Contracts, dApps, Decentralized Systems"),
    ("blank", ""),
    ("Now",     "Sorabbyngo - AI infrastructure"),
    ("",        "Novela - AI assistant platform"),
    ("blank", ""),
    ("Open to", "Research collaborations,"),
    ("",        "engineering discussions,"),
    ("",        "strategic opportunities"),
]

FS, LH, CW = 10, 12, 6.0
PAD, GAP, KEY = 24, 36, 11
art_w = max(len(l) for l in art) * CW
info_x = PAD + art_w + GAP
info_w = max(KEY + len(v) for k, v in info) * CW
W = round(info_x + info_w + PAD)
H = len(art) * LH + PAD * 2
block = len(info) + 2                      # info lines + palette rows
top = PAD + FS + max(0, (len(art) - block) // 2) * LH
e = html.escape

out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="charles@sorabbyngo fastfetch">',
 '<style>text{font-family:"DejaVu Sans Mono",Menlo,Consolas,"Liberation Mono",monospace;font-size:10px;white-space:pre}'
 '.art{fill:#7aa2f7}.k{fill:#bb9af7;font-weight:bold}.v{fill:#c0caf5}.t{fill:#9ece6a;font-weight:bold}.r{fill:#565f89}</style>',
 f'<rect width="100%" height="100%" rx="10" fill="#1a1b26"/>']

for i, line in enumerate(art):
    if line.strip():
        out.append(f'<text class="art" x="{PAD}" y="{PAD + FS + i*LH}" xml:space="preserve">{e(line)}</text>')

for i, (k, v) in enumerate(info):
    y = top + i * LH
    if k == "title":
        out.append(f'<text class="t" x="{info_x}" y="{y}">{e(v)}</text>')
    elif k == "rule":
        out.append(f'<text class="r" x="{info_x}" y="{y}">{v}</text>')
    elif k != "blank":
        out.append(f'<text x="{info_x}" y="{y}" xml:space="preserve">'
                   f'<tspan class="k">{e(k.ljust(KEY))}</tspan><tspan class="v">{e(v)}</tspan></text>')

y = top + len(info) * LH + 4
cols = ["#f7768e","#9ece6a","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#c0caf5","#414868"]
for i, c in enumerate(cols):
    out.append(f'<rect x="{info_x + i*20}" y="{y-9}" width="20" height="12" fill="{c}"/>')

out.append('</svg>')
open("fastfetch.svg", "w", encoding="utf-8").write("\n".join(out))
print("fastfetch.svg", W, "x", H)
