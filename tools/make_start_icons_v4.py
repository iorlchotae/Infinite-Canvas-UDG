"""START.BAT 图标方案（第四轮）：参考 layers.ico / audio.ico 的「浅灰方砖 + 深灰扁平图形 + 单色强调」语言，
强调色由蓝改为联创红 #C8102E，主题全部围绕「画板」。6 组设计：
  D1 层叠画板   三块等距叠放的菱形画板，最前一块红色实底 + 白色播放键（layers 的画布版）
  D2 画板播放   深灰圆角画板 + 白色播放键，右上角红色像素角标（新画布）
  D3 画框取景   三层同心圆角画框 + 红色播放键（取景器/画框层次）
  D4 无限画板   四角深灰扩张括号 + 中央红色画板核心（无限画布展开）
  D5 UDG 徽标   深灰 UDG 字标 + 红色播放键后缀
  D6 画笔落点   45 度深灰画笔 + 笔尖红色触点
输出（项目根 icons/）：
  v4-preview-{1..6}.png   256px 预览
  v4-proposal-{1..6}.ico  多尺寸图标（16/24/32/48/64/128/256）
  v4-sheet.png            浅/深底对比总览
  v4-small_*.png          16/20/24/32/48px 小尺寸可读性测试
用法：./python/python.exe tools/make_start_icons_v4.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(OUT, exist_ok=True)

S = 1024
RED = (200, 16, 46, 255)
WHITE = (255, 255, 255, 255)
GRAY = (84, 86, 91, 255)
TILE = (244, 245, 247, 255)
EDGE = (226, 229, 234, 255)
RADIUS = 0.225
FONT_CANDIDATES = ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/msyhbd.ttc"]


def base():
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, S - 1, S - 1], radius=int(S * RADIUS), fill=TILE)
    d.rounded_rectangle([int(S * 0.006)] * 2 + [S - 1 - int(S * 0.006)] * 2,
                        radius=int(S * (RADIUS - 0.008)), outline=EDGE, width=int(S * 0.009))
    return im


def play(d, cx, cy, w, h, color):
    x0, y0 = cx - w / 2, cy - h / 2
    d.polygon([(x0 + w * 0.16, y0), (x0 + w, cy), (x0 + w * 0.16, y0 + h)], fill=color)


def rot_square(size, radius, angle, fill=None, outline=None, width=0):
    """圆角正方形旋转后的图层（用于菱形画板）。"""
    pad = int(size * 0.8)
    lay = Image.new("RGBA", (size + pad * 2, size + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([pad, pad, pad + size, pad + size], radius=radius,
                         fill=fill, outline=outline, width=width)
    return lay.rotate(angle, expand=True, resample=Image.BICUBIC)


# ---------- D1 层叠画板：三块菱形画板，最前一块红底白播放键 ----------
def d1():
    im = base(); d = ImageDraw.Draw(im)
    bs = S * 0.42
    stroke = int(S * 0.038)
    layers = [(-S * 0.115, GRAY, None), (0.0, GRAY, None), (S * 0.115, RED, WHITE)]
    for dy, col, key in layers:
        lay = rot_square(int(bs), int(bs * 0.16), 45,
                         fill=(col if key else None), outline=(None if key else col),
                         width=stroke)
        im.alpha_composite(lay, (int(S / 2 - lay.width / 2), int(S / 2 + dy - lay.height / 2)))
    play(d, S / 2, S * 0.615, S * 0.165, S * 0.185, WHITE)
    return im


# ---------- D2 画板播放：深灰画板 + 白播放键 + 红色像素角标 ----------
def d2():
    im = base(); d = ImageDraw.Draw(im)
    bs = S * 0.52
    d.rounded_rectangle([S / 2 - bs / 2, S / 2 - bs / 2, S / 2 + bs / 2, S / 2 + bs / 2],
                        radius=int(S * 0.14), fill=GRAY)
    play(d, S / 2, S / 2, S * 0.20, S * 0.225, WHITE)
    b = S * 0.105
    bx, by = S / 2 + bs / 2 - b / 2, S / 2 - bs / 2 - b / 2
    d.rounded_rectangle([bx, by, bx + b, by + b], radius=int(S * 0.026), fill=RED)
    return im


# ---------- D3 画框取景：三层同心画框 + 红色播放键 ----------
def d3():
    im = base(); d = ImageDraw.Draw(im)
    for size in (0.62, 0.46, 0.30):
        half = S * size / 2
        d.rounded_rectangle([S / 2 - half, S / 2 - half, S / 2 + half, S / 2 + half],
                            radius=int(S * size * 0.17), outline=GRAY, width=int(S * 0.036))
    play(d, S / 2, S / 2, S * 0.115, S * 0.13, RED)
    return im


# ---------- D4 无限画板：四角扩张括号 + 中央红色画板核心 ----------
def d4():
    im = base(); d = ImageDraw.Draw(im)
    cs = S * 0.24
    d.rounded_rectangle([S / 2 - cs / 2, S / 2 - cs / 2, S / 2 + cs / 2, S / 2 + cs / 2],
                        radius=int(S * 0.055), fill=RED)
    half = S * 0.33
    arm = S * 0.165
    w = int(S * 0.046)
    r = w / 2
    for sx, sy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        x, y = S / 2 + sx * half, S / 2 + sy * half
        d.line([x, y, x + sx * arm, y], fill=GRAY, width=w)
        d.line([x, y, x, y + sy * arm], fill=GRAY, width=w)
        for px, py in ((x, y), (x + sx * arm, y), (x, y + sy * arm)):
            d.ellipse([px - r, py - r, px + r, py + r], fill=GRAY)
    return im


# ---------- D5 UDG 徽标：深灰字标 + 红色播放键后缀 ----------
def d5():
    im = base(); d = ImageDraw.Draw(im)
    font = None
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            font = ImageFont.truetype(path, int(S * 0.30))
            break
    if font is None:
        font = ImageFont.load_default()
    text = "UDG"
    tw = d.textlength(text, font=font)
    gap, pw = S * 0.11, S * 0.145
    x0 = S / 2 - (tw + gap + pw) / 2
    d.text((x0, S / 2), text, font=font, fill=GRAY, anchor="lm")
    play(d, x0 + tw + gap + pw / 2, S / 2, pw, S * 0.16, RED)
    return im


# ---------- D6 画笔落点：45 度深灰画笔 + 笔尖红色触点 ----------
def d6():
    im = base(); d = ImageDraw.Draw(im)
    import math
    L, bw = S * 0.40, S * 0.115
    tip = S * 0.14
    ax, ay = math.cos(math.radians(45)), -math.sin(math.radians(45))  # 指向右上
    cx = cy = S / 2
    # 笔身：旋转圆角矩形
    pad = int(bw)
    lay = Image.new("RGBA", (int(L) + pad * 2, int(bw) + pad * 2), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.rounded_rectangle([pad, pad, pad + L, pad + bw], radius=bw / 2, fill=GRAY)
    lay = lay.rotate(45, expand=True, resample=Image.BICUBIC)
    im.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))
    # 笔尖三角（底边垂直于笔身轴线）
    hx, hy = cx + ax * L / 2, cy + ay * L / 2
    apexx, apexy = cx + ax * (L / 2 + tip), cy + ay * (L / 2 + tip)
    px, py = ay, -ax  # 轴线的垂直方向
    p1 = (hx + px * bw / 2, hy + py * bw / 2)
    p2 = (hx - px * bw / 2, hy - py * bw / 2)
    d.polygon([(apexx, apexy), p1, p2], fill=GRAY)
    # 笔尖红色触点
    dr = S * 0.048
    dx, dy = cx + ax * (L / 2 + tip + dr * 0.9), cy + ay * (L / 2 + tip + dr * 0.9)
    d.ellipse([dx - dr, dy - dr, dx + dr, dy + dr], fill=RED)
    return im


PROPOSALS = [
    ("1", "D1 层叠画板", d1),
    ("2", "D2 画板播放", d2),
    ("3", "D3 画框取景", d3),
    ("4", "D4 无限画板", d4),
    ("5", "D5 UDG 徽标", d5),
    ("6", "D6 画笔落点", d6),
]
SIZES = [16, 24, 32, 48, 64, 128, 256]
BG_LIGHT = (245, 246, 248, 255)
BG_DARK = (32, 36, 44, 255)

for key, _n, fn in PROPOSALS:
    master = fn()
    master.resize((256, 256), Image.LANCZOS).save(os.path.join(OUT, f"v4-preview-{key}.png"))
    master.resize((256, 256), Image.LANCZOS).save(
        os.path.join(OUT, f"v4-proposal-{key}.ico"), sizes=[(s, s) for s in SIZES])
    print(f"[ok] v4-proposal-{key}.ico / v4-preview-{key}.png")

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
    sheet.save(os.path.join(OUT, f"v4-small_{bgname}.png"))

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
            f = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 20)
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
sheet.save(os.path.join(OUT, "v4-sheet.png"))
print("[ok] v4-sheet.png / v4-small_*.png")
