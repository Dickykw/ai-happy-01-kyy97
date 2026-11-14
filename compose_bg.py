#!/usr/bin/env python3
"""ai-happy-01 session9: v9 Sunny with BACKGROUND variations.
Same note text + same robot drawing (draw-3-nametag) + same layout as v9.
Only the background/setting changes — clean A/B test of background effect.

Themes:
  A kitchen-warm : honey-amber fridge, warm lamp glow top-right
  B bedroom      : soft lavender-pink wall, faint stars/dots, no seam
  C evening-teal : deep teal fridge, warm lamp glow top-left, high contrast
  D sunny-yellow : sunny yellow wall, soft sun rays from top center
Usage: python3 compose_bg.py <theme> <output.png>
"""
import math, random, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
DRAW_SRC = "candidates/draw-3-nametag.jpg"

PAPER = (253, 248, 232)
INK = (45, 65, 130)
INK_SOFT = (70, 90, 150)
LINE_BLUE = (190, 200, 225)
HIGHLIGHT = (255, 232, 120)
TAPE = (235, 220, 185)

THEMES = {
    "A": dict(name="kitchen-warm", bg=(245, 214, 160), dark=(228, 192, 135),
              texture="lines", seam=True, glow=(255, 200, 110, 90), glow_xy=(820, 120)),
    "B": dict(name="bedroom", bg=(233, 214, 236), dark=(215, 193, 219),
              texture="dots", seam=False, glow=(255, 190, 220, 70), glow_xy=(512, 200)),
    "C": dict(name="evening-teal", bg=(38, 84, 98), dark=(27, 62, 76),
              texture="lines", seam=True, glow=(255, 190, 90, 110), glow_xy=(200, 110)),
    "D": dict(name="sunny-yellow", bg=(255, 222, 118), dark=(240, 200, 88),
              texture="rays", seam=False, glow=(255, 245, 180, 80), glow_xy=(512, 60)),
}

def wrap_text(text, font, max_width, draw_obj):
    lines = []
    for para in text.split('\n'):
        if not para:
            lines.append(''); continue
        words = para.split(' ')
        cur = ''
        for w in words:
            test = cur + (' ' if cur else '') + w
            bbox = draw_obj.textbbox((0, 0), test, font=font)
            if bbox[2] - bbox[0] <= max_width:
                cur = test
            else:
                if cur: lines.append(cur)
                cur = w
        if cur: lines.append(cur)
    return lines

def draw_tape(draw, x, y, w, h, angle=0):
    tape = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    td = ImageDraw.Draw(tape)
    td.rectangle([0, 0, w - 1, h - 1], fill=TAPE + (175,), outline=(200, 185, 150, 200))
    tape = tape.rotate(angle, expand=True, center=(w // 2, h // 2))
    draw._image.paste(tape, (x - tape.width // 2 + w // 2, y - tape.height // 2 + h // 2), tape)

def pin(draw, x, y, color):
    draw.ellipse([x - 11, y - 11, x + 11, y + 11], fill=color, outline=(0, 0, 0, 60))
    draw.ellipse([x - 6, y - 7, x + 2, y + 1], fill=(255, 255, 255, 120))

def draw_background(canvas, theme):
    draw = ImageDraw.Draw(canvas)
    bg, dark = theme["bg"], theme["dark"]
    # texture
    if theme["texture"] == "lines":
        for y in range(0, H, 4):
            shade = tuple(max(0, c - 4 + (y // 4) % 2 * 3) for c in bg)
            draw.line([(0, y), (W, y)], fill=shade, width=1)
    elif theme["texture"] == "dots":
        random.seed(11)
        for _ in range(140):
            x = random.randint(0, W); y = random.randint(0, H)
            r = random.randint(2, 5)
            c = tuple(max(0, v - 12) for v in bg)
            draw.ellipse([x - r, y - r, x + r, y + r], fill=c)
        # a few tiny stars
        for _ in range(24):
            x = random.randint(20, W - 20); y = random.randint(20, H - 20)
            draw.text((x, y), "*", fill=(255, 255, 255, 200), font=ImageFont.truetype("Caveat.ttf", 22))
    elif theme["texture"] == "rays":
        cx, cy = W // 2, -60
        for a in range(0, 360, 12):
            ang = math.radians(a)
            x2 = cx + math.cos(ang) * 1400
            y2 = cy + math.sin(ang) * 1400
            col = tuple(min(255, c + 14) for c in bg)
            draw.polygon([(cx, cy), (x2, y2),
                          (cx + math.cos(ang + math.radians(5)) * 1400,
                           cy + math.sin(ang + math.radians(5)) * 1400)], fill=col)
    if theme["seam"]:
        draw.line([(28, 0), (28, H)], fill=dark, width=3)
        draw.line([(31, 0), (31, H)], fill=(245, 242, 236), width=1)
    # warm lamp glow (soft radial)
    gx, gy = theme["glow_xy"]
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r in range(420, 0, -12):
        a = int(theme["glow"][3] * (1 - r / 420) * 0.55)
        gd.ellipse([gx - r, gy - r, gx + r, gy + r], fill=theme["glow"][:3] + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=40))
    canvas.paste(glow, (0, 0), glow)

def main():
    theme_key = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else f"bg-{theme_key.lower()}.png"
    theme = THEMES[theme_key]

    font = ImageFont.truetype("Caveat.ttf", 40)
    font_small = ImageFont.truetype("Caveat.ttf", 34)
    font_cap = ImageFont.truetype("Caveat.ttf", 32)
    font_big = ImageFont.truetype("Caveat.ttf", 46)

    canvas = Image.new("RGB", (W, H), theme["bg"])
    draw = ImageDraw.Draw(canvas)
    draw_background(canvas, theme)
    draw = ImageDraw.Draw(canvas)

    # --- NOTE paper (top) — identical to v9 ---
    pm = 64
    pw = W - 2 * pm
    ph = 470
    px, py = pm, 30
    shadow = Image.new("RGB", (pw + 10, ph + 10), (170, 163, 150))
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=6))
    canvas.paste(shadow, (px - 5, py - 3))
    paper = Image.new("RGB", (pw, ph), PAPER)
    pd = ImageDraw.Draw(paper)
    y = 52
    while y < ph - 10:
        pd.line([(24, y), (pw - 24, y)], fill=LINE_BLUE, width=1)
        y += 40
    pd.line([(52, 0), (52, ph)], fill=(225, 150, 150), width=1)
    paper = paper.rotate(-1.0, expand=False, center=(pw // 2, ph // 2), fillcolor=PAPER)
    canvas.paste(paper, (px, py))

    note = (
        "dear judge,\n"
        "everybody calls you judge.\n"
        "that is not a name.\n"
        "so i named you sunny.\n"
        "hi sunny.\n"
        "love, nia (5)\n"
        "p.s. sunny means you make the sun come out.\n"
        "i checked. it is true.\n"
        "p.p.s. do not tell the other judges.\n"
        "they do not have names yet."
    )
    tmp = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap_text(note, font, pw - 150, tmp)
    key = "so i named you sunny."
    tx, ty = px + 78, py + 18
    y = ty
    key_y = None
    for ln in lines:
        if ln.strip() == key:
            key_y = y
        y += 40
    if key_y is not None:
        bbox = tmp.textbbox((0, 0), key, font=font_big)
        kw = bbox[2] - bbox[0]
        hl = Image.new("RGBA", (kw + 24, 44), (0, 0, 0, 0))
        hd = ImageDraw.Draw(hl)
        hd.rectangle([0, 2, kw + 24, 42], fill=HIGHLIGHT + (255,))
        hl = hl.rotate(-1.0, expand=False, center=((kw + 24) // 2, 22))
        canvas.paste(hl, (tx - 8, key_y - 2), hl)

    random.seed(99)
    y = ty
    for ln in lines:
        if ln == "":
            y += 40; continue
        f = font_big if ln.strip() == key else (font_small if ln.startswith("p.") else font)
        jx = random.randint(-2, 3); jy = random.randint(-1, 2)
        draw.text((tx + jx, y + jy), ln, fill=INK, font=f)
        y += 40

    draw_tape(draw, px + 40, py - 6, 70, 24, angle=-4)
    draw_tape(draw, px + pw - 110, py - 6, 70, 24, angle=4)
    pin(draw, px + 18, py + 14, (220, 60, 60))
    pin(draw, px + pw - 18, py + 14, (60, 110, 220))

    # --- DRAWING (bottom): robot — identical to v9 ---
    dimg = Image.open(DRAW_SRC).convert("RGB")
    dw, dh = dimg.size
    target_w = 440
    target_h = int(target_w * dh / dw)
    dimg = dimg.resize((target_w, target_h), Image.LANCZOS)
    border = 14
    sheet = Image.new("RGB", (target_w + 2 * border, target_h + 2 * border + 44), (250, 248, 242))
    sheet.paste(dimg, (border, border))
    sd = ImageDraw.Draw(sheet)
    sd.text((sheet.width // 2, target_h + 2 * border + 4), "sunny (the judge)",
            fill=INK_SOFT, font=font_cap, anchor="ma")
    sheet = sheet.rotate(1.5, expand=False, center=(sheet.width // 2, sheet.height // 2),
                         fillcolor=(250, 248, 242))
    sh = Image.new("RGBA", (sheet.width + 16, sheet.height + 16), (0, 0, 0, 0))
    shd = ImageDraw.Draw(sh)
    shd.rectangle([8, 8, sh.width - 9, sh.height - 9], fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(radius=7))
    sx = (W - sheet.width) // 2
    sy = py + ph + 28
    canvas.paste(sh, (sx - 8, sy - 4), sh)
    canvas.paste(sheet, (sx, sy))
    draw_tape(draw, sx + sheet.width // 2 - 35, sy - 8, 70, 24, angle=2)
    pin(draw, sx + 16, sy + 12, (60, 180, 90))

    # --- small red heart near note bottom-right ---
    hx, hy = W - 150, py + ph - 46
    draw.ellipse([hx, hy, hx + 22, hy + 20], fill=(230, 70, 70))
    draw.ellipse([hx + 18, hy, hx + 40, hy + 20], fill=(230, 70, 70))
    draw.polygon([(hx + 2, hy + 12), (hx + 38, hy + 12), (hx + 20, hy + 36)], fill=(230, 70, 70))

    # --- vignette ---
    mask = Image.new("L", (W, H), 255)
    md = ImageDraw.Draw(mask)
    cx, cy = W // 2, H // 2
    radius = math.sqrt(W * W + H * H) / 2
    for i in range(256):
        r = radius * (1 - i / 256 * 0.18)
        md.ellipse([cx - r, cy - r, cx + r, cy + r], outline=i, width=4)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=radius * 0.3))
    canvas = Image.composite(canvas, Image.new("RGB", (W, H), (0, 0, 0)), mask)

    canvas.save(output, "PNG", optimize=True)
    import os
    print(f"Done! {output} = {os.path.getsize(output)/1024:.1f} KB, theme={theme['name']}")

if __name__ == "__main__":
    main()
