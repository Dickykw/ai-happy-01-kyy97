#!/usr/bin/env python3
"""Fetch turtle illustration candidates from Pollinations API."""

import urllib.request
import urllib.parse
import os

PROMPT = (
    "Cute cartoon baby turtle, round green shell, big friendly eyes, "
    "happy smile, holding a small yellow daisy flower, "
    "sitting on a wooden desk, warm sunlight, "
    "storybook illustration, simple clean warm background, no text"
)

SEEDS = [5, 12, 19, 26, 33, 44]
WIDTH = 1024
HEIGHT = 1024

def fetch_candidate(seed):
    """Fetch one image from Pollinations, save as cand2-{seed}.jpg."""
    encoded = urllib.parse.quote(PROMPT)
    url = (
        f"https://image.pollinations.ai/prompt/{encoded}"
        f"?width={WIDTH}&height={HEIGHT}&model=flux&nologo=true&seed={seed}"
    )
    filename = f"cand2-{seed}.jpg"
    print(f"  Fetching seed {seed} ... ", end="", flush=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = resp.read()
        with open(filename, "wb") as f:
            f.write(data)
        size_kb = len(data) / 1024
        print(f"OK ({size_kb:.1f} KB)")
        return filename, len(data)
    except Exception as e:
        print(f"FAILED: {e}")
        return None, 0

def crop_bottom(filename, crop_px=60):
    """Crop off bottom crop_px pixels from a JPEG using PIL."""
    try:
        from PIL import Image
        img = Image.open(filename).convert("RGB")
        w, h = img.size
        if h > crop_px:
            img = img.crop((0, 0, w, h - crop_px))
            img.save(filename, "JPEG", quality=95)
            print(f"  Cropped bottom {crop_px}px off {filename} (was {h}, now {h-crop_px})")
        else:
            print(f"  Image too small to crop: {filename}")
    except ImportError:
        print("  PIL not available, skipping crop.")

def main():
    print("=== Fetching turtle candidates (round 2) ===\n")
    results = []
    for seed in SEEDS:
        fn, size = fetch_candidate(seed)
        if fn:
            crop_bottom(fn)
            new_size = os.path.getsize(fn) / 1024
            results.append((fn, new_size))
            print(f"  Final: {fn} = {new_size:.1f} KB\n")
        else:
            results.append((None, 0))

    print("\n=== Summary ===")
    for fn, sz in results:
        if fn:
            print(f"  {fn}: {sz:.1f} KB")
        else:
            print(f"  (seed failed)")

if __name__ == "__main__":
    main()