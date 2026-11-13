#!/usr/bin/env python3
"""
Entrypoint for ai-happy-01.
Copies entry.png to the output directory.
"""

import os
import shutil
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")


def main():
    # Ensure source exists
    if not os.path.isfile(SOURCE):
        print(f"ERROR: source image not found: {SOURCE}", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Copy
    shutil.copyfile(SOURCE, OUTPUT_PATH)

    src_size = os.path.getsize(SOURCE)
    dst_size = os.path.getsize(OUTPUT_PATH)
    print(f"Copied {SOURCE} ({src_size} bytes) -> {OUTPUT_PATH} ({dst_size} bytes)")

    # Validate the output image
    try:
        from PIL import Image
        img = Image.open(OUTPUT_PATH)
        w, h = img.size
        fsize = os.path.getsize(OUTPUT_PATH)
        ok = True
        if fsize > 1_000_000:
            print(f"WARNING: image is {fsize/1024:.1f} KB, exceeds 1 MiB limit")
            ok = False
        if w > 1024 or h > 1024:
            print(f"WARNING: image is {w}x{h}, exceeds 1024x1024 limit")
            ok = False
        if img.format not in ("PNG", "JPEG"):
            print(f"WARNING: image format is {img.format}, expected PNG or JPEG")
            ok = False
        if ok:
            print(f"Validation OK: {w}x{h}, {fsize/1024:.1f} KB, {img.format}")
        else:
            print(f"Validation FAILED — image may not be accepted")
    except ImportError:
        print("PIL not available, skipping validation")
    except Exception as e:
        print(f"Validation error: {e}")


if __name__ == "__main__":
    main()