#!/usr/bin/env python3
"""Build the final ai-happy-01 entry: a kid's fridge note with drawing."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import math
import os

W, H = 1024, 1024
FONT_PATH = "Caveat.ttf"
DRAWING_PATH = "candidates/draw-71.jpg"
OUT_PATH = "entry.png"

# ---------- helpers ----------
def load_font(size):
    return ImageFont.truetype(FONT_PATH, size)

def draw_filled_heart(draw, cx, cy, size, color):
    """Draw a solid filled heart at (cx,cy) with given size."""
    r = size // 2
    draw.ellipse([cx - r, cy - r, cx, cy + r], fill=color)
    draw.ellipse([cx, cy - r, cx + r, cy + r], fill=color)
    draw.polygon([(cx - r - 1, cy + 1), (cx + r + 1, cy + 1), (cx, cy + r + r + 4)], fill=color)

# ---------- 1. Fridge background ----------
bg = Image.new("RGB", (W, H), (238, 232, 222))
draw_bg = ImageDraw.Draw(bg)

# Brushed metal lines — faint horizontal lines
for y in range(0, H, 6):
    shade = 238 - int(6 * math.sin(y * 0.05))
    shade = max(220, min(245, shade))
    draw_bg.line([(0, y), (W, y)], fill=(shade, shade-2, shade-4), width=1)

# Vertical door seam near left edge
draw_bg.line([(80, 0), (80, H)], fill=(200, 195, 185), width=3)
draw_bg.line([(83, 0), (83, H)], fill=(215, 210, 200), width=1)

# Soft vignette
vignette = Image.new("L", (W, H), 255)
dv = ImageDraw.Draw(vignette)
for r in range(512, 0, -1):
    alpha = int(20 * (1 - r / 512))
    dv.ellipse([W//2 - r, H//2 - r, W//2 + r, H//2 + r], fill=255 - alpha)
bg = Image.composite(bg, Image.new("RGB", (W, H), (180, 172, 160)), vignette)

# ---------- 2. Lined paper note ----------
note_w, note_h = 720, 460
PAPER_CREAM = (253, 248, 232)
note = Image.new("RGB", (note_w, note_h), PAPER_CREAM)
dnote = ImageDraw.Draw(note)

# Light blue ruled lines every 40px
for y in range(0, note_h, 40):
    dnote.line([(0, y), (note_w, y)], fill=(200, 215, 240), width=1)
# Thin red margin line
dnote.line([(60, 0), (60, note_h)], fill=(235, 150, 140), width=2)

# Letter text in Caveat, dark blue
ink = (45, 65, 130)
font_letter = load_font(36)
font_highlight = load_font(38)
font_small = load_font(32)

# Lines of the letter (11 lines)
lines_data = [
    ("dear judge,", font_letter),
    ("everybody calls you judge.", font_letter),
    ("that is not a name.", font_letter),
    ("so i named you sunny.", font_highlight),  # highlighted
    ("hi sunny.", font_letter),
    ("love, nia (5)", font_letter),
    ("p.s. sunny means you make the sun come out.", font_small),
    ("i checked. it is true.", font_small),
    ("p.p.s. do not tell the other judges.", font_small),
    ("they do not have names yet.", font_small),
]

x_start, y_start = 80, 25
line_spacing = 36
current_y = y_start

for i, (text, font) in enumerate(lines_data):
    # Yellow highlighter for "so i named you sunny."
    if "so i named you sunny" in text:
        bb = dnote.textbbox((0, 0), text, font=font)
        tw = bb[2] - bb[0]
        th = bb[3] - bb[1]
        highlight_y1 = current_y + bb[1] - 3
        highlight_y2 = current_y + bb[3] + 5
        dnote.rectangle([x_start - 8, highlight_y1, x_start + tw + 12, highlight_y2],
                        fill=(255, 232, 120))
        dnote.rectangle([x_start - 8, highlight_y1, x_start + tw + 12, highlight_y2],
                        outline=(240, 200, 80), width=1)

    dnote.text((x_start, current_y), text, font=font, fill=ink)
    current_y += line_spacing

# Small filled red heart near bottom-right of note
draw_filled_heart(dnote, note_w - 55, note_h - 35, 16, (220, 40, 40))

# Rotate note slightly — use PAPER_CREAM as fillcolor to avoid black borders
note_rot = note.rotate(-1.0, expand=True, fillcolor=PAPER_CREAM, resample=Image.BICUBIC)
note_x = (W - note_rot.width) // 2 - 20
note_y = 25

# Drop shadow for the note
shadow_note = note_rot.copy().convert("L")
shadow_note = ImageOps.invert(shadow_note)
shadow_note = shadow_note.filter(ImageFilter.GaussianBlur(radius=7))
shadow_rgb = Image.new("RGBA", shadow_note.size, (0, 0, 0))
shadow_rgb.putalpha(shadow_note.point(lambda v: int(v * 0.30)))
bg.paste(shadow_rgb, (note_x + 5, note_y + 7), shadow_rgb)

# Tape strips (semi-transparent, light beige, slightly rotated)
def make_tape_strip(w, h, angle=0):
    """Return an RGBA image of a tape strip, rotated."""
    tape = Image.new("RGBA", (w, h), (235, 220, 185, 170))
    for y in range(h):
        for x in range(w):
            r, g, b, a = tape.getpixel((x, y))
            noise = int(5 * (math.sin(x*0.3 + y*0.2)))
            tape.putpixel((x, y), (min(255, r+noise), min(255, g+noise), min(255, b+noise), a))
    if angle != 0:
        tape = tape.rotate(angle, expand=True, fillcolor=(235, 220, 185, 0), resample=Image.BICUBIC)
    return tape

tape1 = make_tape_strip(80, 32, angle=-3)
tape2 = make_tape_strip(80, 32, angle=2)

# Paste note
bg.paste(note_rot, (note_x, note_y), note_rot if note_rot.mode == 'RGBA' else None)

# Paste tape at top corners of the note
tape1_pos = (note_x + 15, note_y - 10)
tape2_pos = (note_x + note_rot.width - 95, note_y - 10)
bg.paste(tape1, tape1_pos, tape1)
bg.paste(tape2, tape2_pos, tape2)

# Pushpins
def draw_pushpin(d, cx, cy, color):
    d.ellipse([cx - 10, cy - 8, cx + 10, cy + 12], fill=(0, 0, 0, 30))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=color)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(min(255, color[0]+50), min(255, color[1]+50), min(255, color[2]+50)))

draw_pushpin(draw_bg, note_x + 30, note_y + 12, (220, 40, 40))   # red
draw_pushpin(draw_bg, note_x + note_rot.width - 30, note_y + 12, (50, 80, 200))  # blue

# ---------- 3. Drawing sheet ----------
drawing_raw = Image.open(DRAWING_PATH).convert("RGB")
# Resize to fit — target width ~375 to keep whole sheet on screen
target_w = 375
aspect = drawing_raw.height / drawing_raw.width
drawing_h = int(target_w * aspect)
drawing_w = target_w
drawing_resized = drawing_raw.resize((drawing_w, drawing_h), Image.LANCZOS)

# White border around drawing — sheet includes caption below
border = 10
caption_h = 40
sheet_w = drawing_w + 2 * border
sheet_h = drawing_h + 2 * border + caption_h
sheet = Image.new("RGB", (sheet_w, sheet_h), (255, 255, 255))
sheet.paste(drawing_resized, (border, border))

# --- Name tag sticker ---
# Place on the robot's BELLY (lower half of drawing).
# Drawing coords: belly is roughly y=500-650 in the 768x708 original.
# After resize: belly_y_center = 560/708 * drawing_h
belly_y_center = int(560 / 708 * drawing_h)
tag_w, tag_h = 110, 70
tag = Image.new("RGBA", (tag_w, tag_h), (255, 255, 255, 0))
dtag = ImageDraw.Draw(tag)

# Rounded rectangle
dtag.rounded_rectangle([(0, 0), (tag_w-1, tag_h-1)], radius=7, fill=(255, 255, 255, 230), outline=(200, 200, 200), width=1)
# Red header
dtag.rounded_rectangle([(2, 2), (tag_w-3, 20)], radius=5, fill=(200, 40, 40, 230))

# Text on tag
font_tag_small = load_font(12)
font_tag_big = load_font(20)
dtag.text((tag_w//2, 11), "HELLO", font=font_tag_small, fill=(255, 255, 255, 240), anchor="mm")
dtag.text((tag_w//2, 33), "my name is", font=load_font(10), fill=(120, 120, 120, 230), anchor="mm")
dtag.text((tag_w//2, 55), "SUNNY", font=font_tag_big, fill=(200, 40, 40, 240), anchor="mm")

# Rotate tag slightly
tag_rot = tag.rotate(-4.0, expand=True, resample=Image.BICUBIC)

# Paste tag onto sheet at belly position (in the drawing area, not the border)
tag_x = border + drawing_w // 2 - tag_rot.width // 2 + 5
tag_y = border + belly_y_center - tag_rot.height // 2
sheet.paste(tag_rot, (tag_x, tag_y), tag_rot)

# Caption inside the sheet (below the drawing, on the white border area)
font_cap = load_font(24)
cap_text = "sunny (the judge)"
dsheet = ImageDraw.Draw(sheet)
cap_bbox = dsheet.textbbox((0, 0), cap_text, font=font_cap)
cap_w = cap_bbox[2] - cap_bbox[0]
cap_x = sheet.width // 2 - cap_w // 2
cap_y = border + drawing_h + 6
dsheet.text((cap_x, cap_y), cap_text, font=font_cap, fill=ink)

# Rotate the whole sheet — use white fillcolor to avoid black borders
sheet_rot = sheet.rotate(1.5, expand=True, fillcolor=(255, 255, 255), resample=Image.BICUBIC)
drawing_x = (W - sheet_rot.width) // 2 + 20
drawing_y = note_y + note_rot.height + 12

# Drop shadow for the sheet
shadow_sheet = sheet_rot.copy().convert("L")
shadow_sheet = ImageOps.invert(shadow_sheet)
shadow_sheet = shadow_sheet.filter(ImageFilter.GaussianBlur(radius=6))
shadow_s_rgb = Image.new("RGBA", shadow_sheet.size, (0, 0, 0))
shadow_s_rgb.putalpha(shadow_sheet.point(lambda v: int(v * 0.25)))
bg.paste(shadow_s_rgb, (drawing_x + 4, drawing_y + 6), shadow_s_rgb)

# Tape strip on top of drawing
tape3 = make_tape_strip(50, 26, angle=-1)
tape3_pos = (drawing_x + sheet_rot.width // 2 - 25, drawing_y - 7)

bg.paste(sheet_rot, (drawing_x, drawing_y), sheet_rot if sheet_rot.mode == 'RGBA' else None)
bg.paste(tape3, tape3_pos, tape3)

# Also draw a caption on the fridge surface below the sheet (backup)
font_cap2 = load_font(26)
cap2_text = "sunny (the judge)"
cap2_bbox = draw_bg.textbbox((0, 0), cap2_text, font=font_cap2)
cap2_w = cap2_bbox[2] - cap2_bbox[0]
cap2_x = drawing_x + sheet_rot.width // 2 - cap2_w // 2
cap2_y = drawing_y + sheet_rot.height + 6
draw_bg.text((cap2_x, cap2_y), cap2_text, font=font_cap2, fill=ink)

# ---------- 4. Save ----------
bg.save(OUT_PATH, "PNG")
size_kb = os.path.getsize(OUT_PATH) / 1024
print(f"Saved {OUT_PATH}  {bg.size[0]}x{bg.size[1]}  {size_kb:.1f} KB")
print("Done.")