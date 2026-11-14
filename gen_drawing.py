#!/usr/bin/env python3
"""Fetch 6 robot illustration candidates from Pollinations API, crop bottom 60px."""

import urllib.request
import urllib.parse
import sys
import os
from PIL import Image
import io

PROMPT = "Cute storybook illustration, a happy little robot with a round white head, big kind closed smiling eyes, rosy cheeks, wearing a big golden crown, red scarf, arms open wide in joy, bright yellow sunburst behind it, warm cheerful colors, clean white background, no text"
SEEDS = [11, 23, 37, 44, 58, 71]
OUT_DIR = "candidates"

os.makedirs(OUT_DIR, exist_ok=True)

for seed in SEEDS:
    params = {
        "prompt": PROMPT,
        "width": 1024,
        "height": 1024,
        "model": "flux",
        "nologo": "true",
        "seed": str(seed),
    }
    url = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(PROMPT) + "?" + urllib.parse.urlencode(params)
    outpath = os.path.join(OUT_DIR, f"draw-{seed}.jpg")
    print(f"Fetching seed {seed}...")
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=60).read()
        img = Image.open(io.BytesIO(data))
        # Crop bottom 60px off (watermark strip)
        w, h = img.size
        img_cropped = img.crop((0, 0, w, h - 60))
        img_cropped.save(outpath, quality=92)
        size_kb = os.path.getsize(outpath) / 1024
        print(f"  Saved {outpath}  ({img_cropped.size[0]}x{img_cropped.size[1]}, {size_kb:.0f} KB)")
    except Exception as e:
        print(f"  FAILED seed {seed}: {e}")

print("Done.")