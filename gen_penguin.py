#!/usr/bin/env python3
"""
Fetch penguin illustration candidates from Pollinations.ai.
Seeds: [3, 11, 17, 23, 31, 47], width=1024, height=1024, model=flux, nologo=true.
Save as candidates/penguin-{seed}.jpg, then crop bottom 60px off each file (remove watermark).
"""

import os
import urllib.request
import urllib.error

from PIL import Image

CANDIDATES_DIR = "candidates"
SEEDS = [3, 11, 17, 23, 31, 47]
PROMPT = (
    "Cute cartoon penguin on a snowy hill throwing a paper plane, "
    "other penguins cheering in the background, bright blue sky, "
    "big friendly eyes, joyful smile, warm sunlight, storybook illustration, "
    "simple clean background, no text"
)
WIDTH = 1024
HEIGHT = 1024
TIMEOUT = 120
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)


def fetch_image(seed: int) -> bytes:
    """Fetch image from Pollinations.ai for the given seed."""
    import urllib.parse
    params = urllib.parse.urlencode({
        "width": WIDTH,
        "height": HEIGHT,
        "seed": seed,
        "model": "flux",
        "nologo": "true",
    })
    url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(PROMPT)}?{params}"
    print(f"  Fetching seed={seed} ...")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        data = resp.read()
    print(f"    Got {len(data)} bytes")
    return data


def crop_bottom(image_path: str, crop_px: int = 60):
    """Crop `crop_px` pixels from the bottom of the JPEG file in-place."""
    img = Image.open(image_path)
    w, h = img.size
    if crop_px >= h:
        print(f"    WARNING: crop_px={crop_px} >= height={h}, skipping crop")
        return
    cropped = img.crop((0, 0, w, h - crop_px))
    cropped.save(image_path, "JPEG", quality=95)
    print(f"    Cropped bottom {crop_px}px, new size: {cropped.size}")


def main():
    os.makedirs(CANDIDATES_DIR, exist_ok=True)

    for seed in SEEDS:
        filename = os.path.join(CANDIDATES_DIR, f"penguin-{seed}.jpg")
        if os.path.exists(filename) and os.path.getsize(filename) > 0:
            print(f"  {filename} already exists ({os.path.getsize(filename)} bytes), skipping fetch")
            continue

        data = fetch_image(seed)
        with open(filename, "wb") as f:
            f.write(data)
        print(f"  Saved {filename} ({len(data)} bytes)")

        crop_bottom(filename, crop_px=60)

    print("\nAll candidates fetched and cropped.")
    for seed in SEEDS:
        path = os.path.join(CANDIDATES_DIR, f"penguin-{seed}.jpg")
        if os.path.exists(path):
            print(f"  {path}: {os.path.getsize(path)} bytes")
        else:
            print(f"  {path}: MISSING")


if __name__ == "__main__":
    main()