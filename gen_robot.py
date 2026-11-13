#!/usr/bin/env python3
"""Fetch 6 robot illustration candidates from Pollinations.ai, crop bottom 60px."""

import os
import urllib.parse
import urllib.request
import urllib.error
from PIL import Image

CANDIDATES_DIR = "candidates"
os.makedirs(CANDIDATES_DIR, exist_ok=True)

PROMPT = (
    "Cute small friendly robot with a hand-drawn smile on its face screen, "
    "holding a red flower, sitting on a wooden desk, a small book beside it, "
    "big friendly eyes, warm golden sunlight, storybook illustration, "
    "simple clean warm background, no text"
)
SEEDS = [5, 9, 16, 24, 33, 41]
WIDTH = 1024
HEIGHT = 1024
TIMEOUT = 120

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

for seed in SEEDS:
    url = (
        f"https://image.pollinations.ai/prompt/{urllib.parse.quote(PROMPT)}"
        f"?width={WIDTH}&height={HEIGHT}&seed={seed}&model=flux&nologo=true"
    )
    out_path = os.path.join(CANDIDATES_DIR, f"robot-{seed}.jpg")
    print(f"Fetching seed {seed} ...")
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            data = resp.read()
        with open(out_path, "wb") as f:
            f.write(data)
        print(f"  Saved {out_path} ({len(data)} bytes)")
    except Exception as e:
        print(f"  FAILED seed {seed}: {e}")
        continue

    # Crop bottom 60 pixels off
    try:
        img = Image.open(out_path)
        w, h = img.size
        # Crop to (left, top, right, bottom)
        cropped = img.crop((0, 0, w, h - 60))
        cropped.save(out_path, quality=95)
        print(f"  Cropped bottom 60px -> {out_path} ({cropped.size})")
    except Exception as e:
        print(f"  Crop FAILED for {out_path}: {e}")

print("Done.")
