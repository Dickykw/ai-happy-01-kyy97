#!/usr/bin/env python3
"""
Draw a cute storybook turtle using pure PIL.
The turtle sits on a desk, facing the viewer, holding a daisy.
"""

import math
from PIL import ImageDraw

def draw_turtle(draw, cx, cy, scale=1.6):
    """
    Draw a cute turtle on the given ImageDraw surface.
    cx, cy = centre of shell.  scale adjusts size.
    """
    # ---- Shell (dome) ----
    sr_x = int(130 * scale)
    sr_y = int(100 * scale)
    # Main shell
    draw.ellipse([cx - sr_x, cy - sr_y, cx + sr_x, cy + sr_y],
                 fill=(100, 155, 80), outline=(60, 120, 45), width=3)
    # Highlight on top-left of shell
    draw.ellipse([cx - 35, cy - 35, cx + 15, cy - 5],
                 fill=(150, 195, 120, 80), outline=None)
    # Rim (lighter band around shell)
    draw.ellipse([cx - sr_x - 8, cy - sr_y - 6,
                  cx + sr_x + 8, cy + sr_y + 6],
                 fill=None, outline=(160, 200, 130), width=4)

    # ---- Hexagon pattern on shell ----
    hex_col = (70, 135, 55)
    hex_centers = [
        (cx - 45, cy - 30), (cx + 35, cy - 35),
        (cx - 10, cy - 10), (cx + 55, cy - 10),
        (cx - 55, cy + 12), (cx + 10, cy + 15),
        (cx - 35, cy + 35), (cx + 40, cy + 30),
    ]
    for hx, hy in hex_centers:
        pts = []
        for a in range(0, 360, 60):
            rad = math.radians(a)
            pts.append((hx + 14 * math.cos(rad), hy + 10 * math.sin(rad)))
        draw.polygon(pts, fill=None, outline=hex_col, width=2)

    # ---- Head ----
    head_cx = cx
    head_cy = cy - sr_y - 22
    draw.ellipse([head_cx - 50, head_cy - 40,
                  head_cx + 50, head_cy + 40],
                 fill=(160, 210, 140), outline=(100, 160, 85), width=2)
    # Head highlight
    draw.ellipse([head_cx - 15, head_cy - 15,
                  head_cx + 5, head_cy + 3],
                 fill=(195, 235, 175, 70))

    # ---- Eyes (BIG, expressive) ----
    for ex in [head_cx - 18, head_cx + 18]:
        ey = head_cy - 6
        # White
        draw.ellipse([ex - 16, ey - 18, ex + 16, ey + 18],
                     fill=(255, 255, 255), outline=(180, 200, 170), width=2)
        # Pupil
        draw.ellipse([ex - 9, ey - 11, ex + 9, ey + 11],
                     fill=(30, 30, 30))
        # Highlight dot
        draw.ellipse([ex + 3, ey - 6, ex + 7, ey + 1],
                     fill=(255, 255, 255))

    # ---- Smile ----
    smile_y = head_cy + 8
    draw.arc([head_cx - 16, smile_y - 4,
              head_cx + 16, smile_y + 10],
             0, 180, fill=(60, 40, 30), width=2)

    # ---- Blush cheeks ----
    draw.ellipse([head_cx - 32, head_cy + 4,
                  head_cx - 14, head_cy + 16],
                 fill=(240, 155, 155, 100))
    draw.ellipse([head_cx + 14, head_cy + 4,
                  head_cx + 32, head_cy + 16],
                 fill=(240, 155, 155, 100))

    # ---- Front flippers ----
    # Left flipper
    fl_lx = cx - sr_x - 12
    fl_ly = cy + 10
    draw.ellipse([fl_lx - 22, fl_ly - 14,
                  fl_lx + 12, fl_ly + 14],
                 fill=(140, 190, 120), outline=(100, 155, 85), width=2)
    # Right flipper (holds flower)
    fl_rx = cx + sr_x + 12
    fl_ry = cy + 5
    draw.ellipse([fl_rx - 12, fl_ry - 14,
                  fl_rx + 22, fl_ry + 14],
                 fill=(140, 190, 120), outline=(100, 155, 85), width=2)

    # ---- Feet ----
    foot_y = cy + sr_y + 12
    for fx in [cx - 40, cx + 40]:
        draw.ellipse([fx - 24, foot_y - 10,
                      fx + 24, foot_y + 10],
                     fill=(130, 180, 110), outline=(90, 145, 75), width=2)
        # Tiny toes
        for tx in [-12, 0, 12]:
            draw.ellipse([fx + tx - 5, foot_y + 8,
                          fx + tx + 5, foot_y + 14],
                         fill=(100, 155, 85))

    # ---- Tiny tail ----
    tail_x, tail_y = cx, cy + sr_y + 6
    draw.polygon([(tail_x - 5, tail_y),
                  (tail_x + 5, tail_y),
                  (tail_x, tail_y + 20)],
                 fill=(100, 155, 80), outline=(70, 120, 55), width=1)

    # ---- Daisy in right flipper (bigger, brighter) ----
    stem_x = fl_rx + 14
    stem_y = fl_ry - 5
    # Stem
    for dy in range(0, 48):
        sx = stem_x + int(math.sin(dy * 0.15) * 3)
        sy = stem_y - dy
        if 0 <= sx < 2000 and 0 <= sy < 2000:
            draw.ellipse([sx-2, sy-1, sx+2, sy+1], fill=(70, 140, 55))
    # Flower centre
    fx_, fy_ = stem_x, stem_y - 48
    # Petals (white, more of them, bigger)
    for a in range(0, 360, 20):
        rad = math.radians(a)
        px = fx_ + int(math.cos(rad) * 16)
        py = fy_ + int(math.sin(rad) * 16)
        for dx in range(-7, 8):
            for dy in range(-7, 8):
                if dx * dx + dy * dy <= 35:
                    cx2, cy2 = px + dx, py + dy
                    if 0 <= cx2 < 2000 and 0 <= cy2 < 2000:
                        draw.point((cx2, cy2), fill=(255, 248, 235))
    # Petal outline (subtle)
    for a in range(0, 360, 20):
        rad = math.radians(a)
        px = fx_ + int(math.cos(rad) * 16)
        py = fy_ + int(math.sin(rad) * 16)
        for dx in range(-7, 8):
            for dy in range(-7, 8):
                if 30 <= dx * dx + dy * dy <= 36:
                    cx2, cy2 = px + dx, py + dy
                    if 0 <= cx2 < 2000 and 0 <= cy2 < 2000:
                        draw.point((cx2, cy2), fill=(230, 220, 210))
    # Yellow centre (bigger, brighter)
    for dx in range(-9, 10):
        for dy in range(-9, 10):
            if dx * dx + dy * dy <= 55:
                cx2, cy2 = fx_ + dx, fy_ + dy
                if 0 <= cx2 < 2000 and 0 <= cy2 < 2000:
                    draw.point((cx2, cy2), fill=(255, 215, 40))
    # Centre highlight
    for dx in range(-4, 5):
        for dy in range(-4, 5):
            if dx * dx + dy * dy <= 10:
                cx2, cy2 = fx_ + dx, fy_ + dy
                if 0 <= cx2 < 2000 and 0 <= cy2 < 2000:
                    draw.point((cx2, cy2), fill=(255, 240, 90))