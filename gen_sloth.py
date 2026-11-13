#!/usr/bin/env python3
"""Fetch sloth illustration candidates from Pollinations.ai and save them."""

import urllib.request
import urllib.error
import sys
import os
from PIL import Image

POLLINATIONS_BASE = "https://image.pollinations.ai/prompt/"
PROMPT = "Cute cartoon sloth hanging upside down from a tree branch, holding a tiny red knitted scarf, ball of red yarn nearby, big friendly sleepy eyes, gentle smile, warm golden sunlight, storybook illustration, simple clean warm background, no text"
SEEDS = [7, 14, 21, 28, 35, 42]
WIDTH = 1024
HEIGHT = 1024
CROP_BOTTOM = 60  # pixels to remove from bottom (watermark area)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_image(seed: int, outpath: str) -> bool:
    """Fetch one image from Pollinations and save to outpath. Returns True on success."""
    # Build URL with parameters
    url = (
        f"{POLLINATIONS_BASE}{urllib.request.quote(PROMPT)}"
        f"?seed={seed}&width={WIDTH}&height={HEIGHT}"
        f"&model=flux&nologo=true"
    )
    print(f"  Fetching seed={seed} ...", end=" ", flush=True)
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        if not data:
            print("EMPTY response")
            return False
        # Save raw image
        with open(outpath, "wb") as f:
            f.write(data)
        print(f"OK ({len(data)} bytes)", flush=True)
        return True
    except Exception as e:
        print(f"FAILED: {e}", flush=True)
        return False


def crop_bottom(inpath: str, outpath: str, crop_px: int):
    """Crop bottom crop_px pixels off the image using PIL."""
    img = Image.open(inpath)
    w, h = img.size
    if crop_px >= h:
        print(f"  WARNING: crop_px={crop_px} >= height={h}, skipping crop")
        img.save(outpath)
        return
    cropped = img.crop((0, 0, w, h - crop_px))
    cropped.save(outpath)
    print(f"  Cropped bottom {crop_px}px: {inpath} -> {outpath} (size={w}x{h-crop_px})")


def main():
    print(f"Fetching {len(SEEDS)} sloth candidates from Pollinations.ai ...")
    print(f"Prompt: {PROMPT[:80]}...\n")

    os.makedirs("candidates", exist_ok=True)

    for seed in SEEDS:
        raw_path = f"candidates/sloth-{seed}.raw.jpg"
        final_path = f"candidates/sloth-{seed}.jpg"
        ok = fetch_image(seed, raw_path)
        if ok:
            crop_bottom(raw_path, final_path, CROP_BOTTOM)
            # Remove raw file
            if os.path.exists(raw_path):
                os.remove(raw_path)
        else:
            print(f"  SKIPPING seed={seed}")

    # Report final files
    print("\nFinal candidate files:")
    for seed in SEEDS:
        path = f"candidates/sloth-{seed}.jpg"
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  {path}: {size} bytes")
        else:
            print(f"  {path}: MISSING")


if __name__ == "__main__":
    main()