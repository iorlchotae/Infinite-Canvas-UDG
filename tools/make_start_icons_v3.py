"""START.BAT 图标方案（第三轮）：以 C「像素汇聚」为基底的 5 个衍生设计。
保留 C 的 DNA：白底圆角方块 + 联创红 #C8102E 像素块 + 播放键，改变的是像素与播放键的关系。
输出（项目根 icons/）：
  v3-preview-{1..5}.png   256px 预览
  v3-proposal-{1..5}.ico  多尺寸图标（16/24/32/48/64/128/256）
  v3-sheet.png            浅/深底对比总览
  v3-small_*.png          16/20/24/32/48px 小尺寸可读性测试
用法：./python/python.exe tools/make_start_icons_v3.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

S = 1024
RED = (200, 16, 46, 255)
WHITE = (255, 255, 255, 255)
HAIR = (228, 231, 236, 255)
RADIUS = 0.225
FONT_CN = "C:/Windows/Fonts/msyhbd.ttc"
CELL, GAP = S * 0.19, S * 0.07          # 2x2 网格单元与间距
GRID = CELL * 2 + GAP
X0 = (S - GRID) / 2
Y0 = (S - GRID) / 2

def base():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * RADIUS), fill=WHITE)
    d.rounded_rectangle([int(S * 0.006)] * 2 + [S - 1 - int(S * 0.006)] * 2,
                        radius=int(S * (RADIUS - 0.008)), outline=HAIR, width=int(S * 0.012))
    return im

def play(d, cx, cy, w, h, color):
    x0, y0 = cx - w / 2, cy - h / 2
    d.polygon([(x0 + w * 0.16, y0), (x0 + w, cy), (x0 + w * 0.16, y0 + h)], fill=color)

def pixel(d, cx, cy, size, color=RED, hollow=False, width=None):
    half = size / 2
    if hollow:
        d.rounded_rectangle([cx - half, cy - half, cx + half, cy + half],
                            radius=int(size * 0.26), outline=color,
                            width=width or int(S * 0.024))
    else:
        d.rounded_rectangle([cx - half, cy - half, cx + half, cy + half],
                            radius=int(size * 0.26), fill=color)

def cell_center(i, j):
    return X0 + i * (CELL + GAP) + CELL / 2, Y0 + j * (CELL + GAP) + CELL / 2

# ---------- C1 基准：三颗红像素，第四格长成红色播放键 ----------
def c1():
    im = base(); d = ImageDraw.Draw(im)
    for i in range(2):
        for j in range(2):
            cx, cy = cell_center(i, j)
            if i == 1 and j == 1:
                play(d, cx + CELL * 0.04, cy, CELL * 0.92, CELL * 1.0, RED)
            else:
                pixel(d, cx, cy, CELL)
    return im

# ---------- C2 生长：第四格放大成红色按键，内嵌白色播放键 ----------
def c2():
    im = base(); d = ImageDraw.Draw(im)
    for i in range(2):
        for j in range(2):
            cx, cy = cell_center(i, j)
            if i == 1 and j == 1:
                pixel(d, cx, cy, CELL * 1.45)                 # 像素长大
                play(d, cx, cy, CELL * 0.72, CELL * 0.80, WHITE)  # 键心反白
            else:
                pixel(d, cx, cy, CELL)
    return im

# ---------- C3 破格：播放键放大并探出网格，向外发力 ----------
def c3():
    im = base(); d = ImageDraw.Draw(im)
    for i in range(2):
        for j in range(2):
            cx, cy = cell_center(i, j)
            if i == 1 and j == 1:
                play(d, cx + CELL * 0.10, cy + CELL * 0.04, CELL * 1.18, CELL * 1.30, RED)
            else:
                pixel(d, cx, cy, CELL)
    return im

# ---------- C4 阶梯：三颗像素沿对角线渐大，终点是播放键 ----------
def c4():
    im = base(); d = ImageDraw.Draw(im)
    diag = [(0.30, 0.30, 0.130), (0.50, 0.50, 0.158), (0.70, 0.70, 0.186)]
    for fx, fy, size in diag:
        pixel(d, S * fx, S * fy, S * size)
    play(d, S * 0.80, S * 0.80, S * 0.185, S * 0.215, RED)
    return im

# ---------- C5 空心像素：前三格描边、第四格实心播放键 ----------
def c5():
    im = base(); d = ImageDraw.Draw(im)
    for i in range(2):
        for j in range(2):
            cx, cy = cell_center(i, j)
            if i == 1 and j == 1:
                play(d, cx + CELL * 0.04, cy, CELL * 0.92, CELL * 1.0, RED)
            else:
                pixel(d, cx, cy, CELL, hollow=True)
    return im

PROPOSALS = [
    ("1", "C1 像素汇聚", c1),
    ("2", "C2 生长按键", c2),
    ("3", "C3 破格出发", c3),
    ("4", "C4 阶梯加速", c4),
    ("5", "C5 空心像素", c5),
]
SIZES = [16, 24, 32, 48, 64, 128, 256]
BG_LIGHT = (245, 246, 248, 255)
BG_DARK = (32, 36, 44, 255)

for key, _n, fn in PROPOSALS:
    master = fn()
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, f"v3-preview-{key}.png"))
    master.resize((256, 256), Image.LANCZOS).save(
        os.path.join(OUT, f"v3-proposal-{key}.ico"), sizes=[(s, s) for s in SIZES])
    print(f"[ok] v3-proposal-{key}.ico / v3-preview-{key}.png")

# 小尺寸可读性测试
for bgname, bg in (("light", BG_LIGHT), ("dark", BG_DARK)):
    pad, cell, gapx, gapy = 8, 48, 18, 16
    sizes = [16, 20, 24, 32, 48]
    w = pad * 2 + len(sizes) * (cell + gapx)
    h = pad * 2 + len(PROPOSALS) * (cell + gapy)
    sheet = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for r, (_k, _n, fn) in enumerate(PROPOSALS):
        ic = fn()
        for ci, px in enumerate(sizes):
            box = Image.new("RGBA", (cell, cell), bg)
            box.alpha_composite(ic.resize((px, px), Image.LANCZOS), ((cell - px) // 2, (cell - px) // 2))
            sheet.alpha_composite(box, (pad + ci * (cell + gapx), pad + r * (cell + gapy)))
    sheet = sheet.resize((sheet.width * 4, sheet.height * 4), Image.NEAREST)
    sheet.save(os.path.join(OUT, f"v3-small_{bgname}.png"))

# 对比总览
ICON_PX, CELL_BOX, PAD, GAP_BOX = 128, 150, 20, 24
rows = []
for bg in (BG_LIGHT, BG_DARK):
    cells = []
    for key, name, fn in PROPOSALS:
        box = Image.new("RGBA", (CELL_BOX, CELL_BOX + 34), bg)
        box.alpha_composite(fn().resize((ICON_PX, ICON_PX), Image.LANCZOS),
                            ((CELL_BOX - ICON_PX) // 2, 0))
        lab = ImageDraw.Draw(box)
        try:
            f = ImageFont.truetype(FONT_CN, 20)
        except Exception:
            f = ImageFont.load_default()
        lab.text((CELL_BOX / 2, CELL_BOX + 17), name, font=f, fill=(30, 34, 40, 255), anchor="mm")
        cells.append(box)
    width = PAD * 2 + len(cells) * CELL_BOX + (len(cells) - 1) * GAP_BOX
    row = Image.new("RGBA", (width, CELL_BOX + 34 + PAD * 2), (0, 0, 0, 0))
    x = PAD
    for cbox in cells:
        row.alpha_composite(cbox, (x, PAD)); x += CELL_BOX + GAP_BOX
    rows.append(row)
sheet = Image.new("RGBA", (rows[0].width, rows[0].height * 2 + 24), (0, 0, 0, 0))
for i, r in enumerate(rows):
    sheet.alpha_composite(r, (0, i * (r.height + 24)))
sheet = sheet.resize((sheet.width * 2, sheet.height * 2), Image.LANCZOS)
sheet.save(os.path.join(OUT, "v3-sheet.png"))
print("[ok] v3-sheet.png / v3-small_*.png")
