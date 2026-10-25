"""START.BAT 图标方案（第二轮）：白底 + 白红相间，保留「圆角画布 + 联创红 #C8102E + UDG」基因。
输出（项目根 icons/）：
  v2-preview-{a,b,c,d}.png   256px 预览
  v2-proposal-{a,b,c,d}.ico  多尺寸图标（16/24/32/48/64/128/256）
  v2-sheet.png               浅/深底对比总览
用法：./python/python.exe tools/make_start_icons_v2.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

S = 1024
RED = (200, 16, 46, 255)        # 联创红 #C8102E
WHITE = (255, 255, 255, 255)
HAIR = (228, 231, 236, 255)     # 白底在浅色资源管理器里的描边（极淡，仅定边）
RADIUS = 0.225
FONT_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_CN = "C:/Windows/Fonts/msyhbd.ttc"

def base():
    """白底圆角方块 + 极淡描边"""
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * RADIUS), fill=WHITE)
    d.rounded_rectangle([int(S * 0.006), int(S * 0.006), S - 1 - int(S * 0.006), S - 1 - int(S * 0.006)],
                        radius=int(S * (RADIUS - 0.008)), outline=HAIR, width=int(S * 0.012))
    return im

def play(d, cx, cy, w, h, color):
    x0, y0 = cx - w / 2, cy - h / 2
    d.polygon([(x0 + w * 0.16, y0), (x0 + w, cy), (x0 + w * 0.16, y0 + h)], fill=color)

def frame(d, m, width, color, radius_ratio=0.075):
    d.rounded_rectangle([m, m, S - m, S - m], radius=int(S * radius_ratio),
                        outline=color, width=width)

# ---------- A 红框播放键：白底 + 红色画框 + 红色播放三角 ----------
def a():
    im = base(); d = ImageDraw.Draw(im)
    frame(d, S * 0.20, int(S * 0.055), RED)
    play(d, S * 0.5, S * 0.5, S * 0.28, S * 0.32, RED)
    return im

# ---------- B 红玉白键：白底 + 中央红色圆角块 + 白色播放三角 ----------
def b():
    im = base(); d = ImageDraw.Draw(im)
    m = S * 0.185
    d.rounded_rectangle([m, m, S - m, S - m], radius=int(S * 0.135), fill=RED)
    play(d, S * 0.5, S * 0.5, S * 0.30, S * 0.34, WHITE)
    return im

# ---------- C 像素汇聚：白底 + 三颗红像素 + 第四格长成红色播放键 ----------
def c():
    im = base(); d = ImageDraw.Draw(im)
    cell, gap = S * 0.19, S * 0.07
    total = cell * 2 + gap
    x0, y0 = (S - total) / 2, (S - total) / 2
    for i in range(2):
        for j in range(2):
            x, y = x0 + i * (cell + gap), y0 + j * (cell + gap)
            if i == 1 and j == 1:      # 右下格：播放键
                play(d, x + cell * 0.54, y + cell / 2, cell * 0.92, cell * 1.0, RED)
            else:
                d.rounded_rectangle([x, y, x + cell, y + cell],
                                    radius=int(cell * 0.26), fill=RED)
    return im

# ---------- D UDG 徽标：白底 + 红色 UDG 字标 + 右下角红色播放键 ----------
def d():
    im = base(); dr = ImageDraw.Draw(im)
    f = ImageFont.truetype(FONT_BOLD, int(S * 0.235))
    dr.text((S * 0.46, S * 0.455), "UDG", font=f, fill=RED, anchor="mm")
    play(dr, S * 0.735, S * 0.70, S * 0.185, S * 0.21, RED)
    return im

PROPOSALS = [
    ("a", "A 红框播放键", a),
    ("b", "B 红玉白键", b),
    ("c", "C 像素汇聚", c),
    ("d", "D UDG徽标", d),
]
SIZES = [16, 24, 32, 48, 64, 128, 256]
BG_LIGHT = (245, 246, 248, 255)
BG_DARK = (32, 36, 44, 255)

for key, _n, fn in PROPOSALS:
    master = fn()
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, f"v2-preview-{key}.png"))
    master.resize((256, 256), Image.LANCZOS).save(
        os.path.join(OUT, f"v2-proposal-{key}.ico"), sizes=[(s, s) for s in SIZES])
    print(f"[ok] v2-proposal-{key}.ico / v2-preview-{key}.png")

# 小尺寸可读性测试（16/20/24/32/48，浅/深底）
for bgname, bg in (("light", BG_LIGHT), ("dark", BG_DARK)):
    pad, cell, gapx, gapy = 8, 48, 18, 16
    sizes = [16, 20, 24, 32, 48]
    w = pad * 2 + len(sizes) * (cell + gapx)
    h = pad * 2 + len(PROPOSALS) * (cell + gapy)
    sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for r, (_k, _n, fn) in enumerate(PROPOSALS):
        ic = fn()
        for cidx, px in enumerate(sizes):
            box = Image.new("RGBA", (cell, cell), bg)
            box.alpha_composite(ic.resize((px, px), Image.LANCZOS), ((cell - px) // 2, (cell - px) // 2))
            sheet.alpha_composite(box, (pad + cidx * (cell + gapx), pad + r * (cell + gapy)))
    sheet = sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST)
    sheet.save(os.path.join(OUT, f"v2-small_{bgname}.png"))

# 对比总览
ICON_PX, CELL, PAD, GAP = 128, 150, 20, 24
rows = []
for bg in (BG_LIGHT, BG_DARK):
    cells = []
    for key, name, fn in PROPOSALS:
        box = Image.new("RGBA", (CELL, CELL + 34), bg)
        box.alpha_composite(fn().resize((ICON_PX, ICON_PX), Image.LANCZOS), ((CELL - ICON_PX) // 2, 0))
        lab = ImageDraw.Draw(box)
        try:
            f = ImageFont.truetype(FONT_CN, 20)
        except Exception:
            f = ImageFont.load_default()
        lab.text((CELL / 2, CELL + 17), name, font=f, fill=(30, 34, 40, 255), anchor="mm")
        cells.append(box)
    width = PAD * 2 + len(cells) * CELL + (len(cells) - 1) * GAP
    row = Image.new("RGBA", (width, CELL + 34 + PAD * 2), (0, 0, 0, 0))
    x = PAD
    for cbox in cells:
        row.alpha_composite(cbox, (x, PAD)); x += CELL + GAP
    rows.append(row)
sheet = Image.new("RGBA", (rows[0].width, rows[0].height * 2 + 24), (0, 0, 0, 0))
for i, r in enumerate(rows):
    sheet.alpha_composite(r, (0, i * (r.height + 24)))
sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS)
sheet.save(os.path.join(OUT, "v2-sheet.png"))
print("[ok] v2-sheet.png / v2-small_*.png")
