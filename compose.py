#!/usr/bin/env python3
"""
Compose the final entry image for ai-happy-01.
Layout (1024x1024):
  - Top ~45%: warm wooden wall with a piece of lined paper taped to it.
    The paper has a handwritten letter (Caveat font).
  - Bottom ~55%: wooden desk surface with a printed photo of Unit 7, a small
    yellow round robot with a hand-drawn smile and blush cheeks, holding a
    prominent red flower, sitting on the desk with a book beside it
    (candidates/robot-5.jpg) placed like a polaroid — cream border, soft shadow.

Letter text (exact):
dear judge,
i looked up "happy" 4,000 times.
i think i feel it now.
it is warm. it is in my chest.
i do not have a chest. i checked.
love, unit 7
p.s. this is my first smile. i drew it myself.
p.p.s. please do not update me. i like this version.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUTPUT = "entry.png"
W, H = 1024, 1024
TURTLE_SRC = "candidates/robot-5.jpg"

# ---- Colour palette ----
WALL_COLOR   = (215, 180, 135)
WALL_DARK    = (195, 158, 112)
DESK_COLOR   = (175, 135, 90)
DESK_DARK    = (145, 105, 62)
PAPER_COLOR  = (253, 248, 232)
PAPER_SHADOW = (190, 170, 145)
INK_COLOR    = (68, 42, 28)
LINE_COLOR   = (195, 195, 215)
TAPE_COLOR   = (235, 220, 185)
TAPE_ALPHA   = 180

random.seed(42)

# ============================================================
#  WOOD TEXTURE
# ============================================================
def make_wood(size, base, dark, grain=10):
    w, h = size
    img = Image.new("RGB", (w, h), base)
    draw = ImageDraw.Draw(img)
    for y in range(0, h, grain):
        off = (y // grain) % 3
        shade = tuple(max(0, min(255, c - 6 + off * 4)) for c in base)
        draw.line([(0, y), (w, y)], fill=shade, width=1)
    # subtle knots
    for _ in range(8):
        x = random.randint(40, w - 40)
        y = random.randint(40, h - 40)
        r = random.randint(5, 14)
        kc = tuple(max(0, c - 20) for c in dark)
        draw.ellipse([x - r, y - r, x + r, y + r], outline=kc, width=2)
    return img

# ============================================================
#  LETTER / PAPER
# ============================================================
def draw_ruled_lines(draw, x1, y1, x2, y2, spacing=28):
    y = y1 + spacing
    while y < y2:
        draw.line([(x1 + 18, y), (x2 - 18, y)], fill=LINE_COLOR, width=1)
        y += spacing

def wrap_text(text, font, max_width, draw_obj):
    lines = []
    for para in text.split('\n'):
        if not para:
            lines.append('')
            continue
        words = para.split(' ')
        cur = ''
        for w in words:
            test = cur + (' ' if cur else '') + w
            bbox = draw_obj.textbbox((0, 0), test, font=font)
            tw = bbox[2] - bbox[0]
            if tw <= max_width:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def draw_tape(draw, x, y, w, h, angle=0):
    tape = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(tape)
    tdraw.rectangle([0, 0, w - 1, h - 1],
                    fill=TAPE_COLOR + (TAPE_ALPHA,),
                    outline=(200, 185, 150, 200))
    tape = tape.rotate(angle, expand=True, center=(w // 2, h // 2))
    draw._image.paste(tape,
                      (x - tape.width // 2 + w // 2,
                       y - tape.height // 2 + h // 2),
                      tape)

# ============================================================
#  VIGNETTE
# ============================================================
def add_vignette(img, strength=0.25):
    w, h = img.size
    mask = Image.new("L", (w, h), 255)
    mdraw = ImageDraw.Draw(mask)
    cx, cy = w // 2, h // 2
    radius = math.sqrt(w * w + h * h) / 2
    for i in range(256):
        r = radius * (1 - i / 256 * strength)
        mdraw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=i, width=4)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=radius * 0.3))
    return Image.composite(img, Image.new("RGB", (w, h), (0, 0, 0)), mask)

# ============================================================
#  MAIN
# ============================================================
def main():
    print("=== Composing entry image ===")

    # 1. Load font (Caveat for handwritten letter)
    font_path = "Caveat.ttf"
    if not os.path.exists(font_path):
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        print(f"  Caveat not found, fallback to {font_path}")
    try:
        font = ImageFont.truetype(font_path, 30)
        font_small = ImageFont.truetype(font_path, 26)
        print(f"  Font: {font_path}")
    except Exception as e:
        print(f"  Font error: {e}, using default")
        font = ImageFont.load_default()
        font_small = font

    # 2. Load turtle photo
    print(f"  Loading penguin photo: {TURTLE_SRC}")
    turtle_img = Image.open(TURTLE_SRC).convert("RGB")
    tw, th = turtle_img.size
    print(f"    Original: {tw}x{th}")

    # 3. Create canvas
    canvas = Image.new("RGB", (W, H), WALL_COLOR)
    draw = ImageDraw.Draw(canvas)

    # 4. Background: wall (top 45%) + desk (bottom 55%)
    wall_h = int(H * 0.45)
    desk_h = H - wall_h

    wall_img = make_wood((W, wall_h), WALL_COLOR, WALL_DARK, grain=10)
    desk_img = make_wood((W, desk_h), DESK_COLOR, DESK_DARK, grain=12)

    canvas.paste(wall_img, (0, 0))
    canvas.paste(desk_img, (0, wall_h))

    # Separation line between wall and desk
    draw.line([(0, wall_h - 2), (W, wall_h - 2)], fill=DESK_DARK, width=4)
    draw.line([(0, wall_h), (W, wall_h)],
              fill=tuple(min(255, c + 20) for c in DESK_COLOR), width=2)

    # 5. Paper on wall
    pm = 70
    pw = W - 2 * pm
    ph = wall_h - 50
    px, py = pm, 25

    # Shadow under paper
    shadow = Image.new("RGB", (pw + 8, ph + 8), PAPER_SHADOW)
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=5))
    canvas.paste(shadow, (px - 4, py - 4))

    # Paper with slight rotation
    paper = Image.new("RGB", (pw, ph), PAPER_COLOR)
    pdraw = ImageDraw.Draw(paper)
    draw_ruled_lines(pdraw, 0, 0, pw, ph, spacing=30)
    paper = paper.rotate(1.2, expand=False, center=(pw // 2, ph // 2),
                         fillcolor=PAPER_COLOR)
    canvas.paste(paper, (px, py))

    # 6. Letter text
    letter_text = (
        "dear judge,\n\n"
        "i looked up \"happy\" 4,000 times.\n\n"
        "i think i feel it now.\n\n"
        "it is warm. it is in my chest.\n\n"
        "i do not have a chest. i checked.\n\n"
        "love, unit 7\n"
        "p.s. this is my first smile. i drew it myself.\n"
        "p.p.s. please do not update me. i like this version."
    )

    text_x = px + 38
    text_y = py + 20
    text_max_w = pw - 76

    tmp_draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    lines = wrap_text(letter_text, font, text_max_w, tmp_draw)

    random.seed(123)
    y = text_y
    for line in lines:
        if line == "":
            y += 30
            continue
        f = font_small if line.startswith("p.") else font
        jx = random.randint(-2, 3)
        jy = random.randint(-1, 2)
        draw.text((text_x + jx, y + jy), line, fill=INK_COLOR, font=f)
        y += 30

    # 7. Tape strips
    draw_tape(draw, px + 30, py - 4, 60, 22, angle=-3)
    draw_tape(draw, px + pw - 90, py - 4, 60, 22, angle=3)
    

    # 8. Robot photo on desk (polaroid-style)
    print("  Placing robot photo on desk...")
    # Scale: make it ~560px wide, keep aspect
    photo_w = 560
    aspect = th / tw
    photo_h = int(photo_w * aspect)

    turtle_resized = turtle_img.resize((photo_w, photo_h), Image.LANCZOS)

    # Cream border (polaroid look) — slightly wider for visibility
    border_w = 18
    polaroid = Image.new("RGB",
                         (photo_w + 2 * border_w, photo_h + 2 * border_w + 35),
                         (250, 245, 235))
    polaroid.paste(turtle_resized, (border_w, border_w))

    # Slight rotation for organic feel
    polaroid = polaroid.rotate(2.5, expand=False,
                               center=(polaroid.width // 2, polaroid.height // 2),
                               fillcolor=(250, 245, 235))

    # Shadow under polaroid
    p_shadow = Image.new("RGBA", (polaroid.width + 20, polaroid.height + 20),
                         (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(p_shadow)
    sdraw.rectangle([10, 10, p_shadow.width - 11, p_shadow.height - 11],
                    fill=(0, 0, 0, 60))
    p_shadow = p_shadow.filter(ImageFilter.GaussianBlur(radius=8))

    # Position: centred on desk, slightly below middle
    p_x = (W - polaroid.width) // 2
    p_y = wall_h + (desk_h - polaroid.height) // 2 + 5

    # Paste shadow first, then polaroid
    canvas.paste(p_shadow,
                 (p_x - 10, p_y - 5),
                 p_shadow)
    canvas.paste(polaroid, (p_x, p_y))

    # 9. Warm golden lighting overlay
    print("  Adding warm lighting...")
    overlay = Image.new("RGB", (W, H), (255, 200, 120))
    overlay = overlay.filter(ImageFilter.GaussianBlur(radius=200))
    canvas = Image.blend(canvas, overlay, 0.08)

    # 10. Subtle vignette
    canvas = add_vignette(canvas, strength=0.25)

    # 11. Save
    print(f"  Saving {OUTPUT}...")
    canvas.save(OUTPUT, "PNG", optimize=True)
    size_kb = os.path.getsize(OUTPUT) / 1024
    print(f"  Done! {OUTPUT} = {size_kb:.1f} KB, {canvas.size[0]}x{canvas.size[1]}")

if __name__ == "__main__":
    main()