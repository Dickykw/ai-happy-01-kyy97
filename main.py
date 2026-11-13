#!/usr/bin/env python3
"""
Entrypoint for ai-happy-01 (make.fun competition).
Copies entry.png to the output directory and validates it.
"""

import os
import sys
from pathlib import Path

SRC = "entry.png"


def validate_image(path: str) -> bool:
    """Check that the image is PNG/JPEG, <= 1024x1024, <= 1 MiB."""
    from PIL import Image

    size = os.path.getsize(path)
    if size > 1_048_576:
        print(f"  FAIL: file size {size} bytes exceeds 1 MiB")
        return False

    img = Image.open(path)
    w, h = img.size
    if w > 1024 or h > 1024:
        print(f"  FAIL: dimensions {w}x{h} exceed 1024x1024")
        return False

    if img.format not in ("PNG", "JPEG", "JPG"):
        print(f"  FAIL: format {img.format} is not PNG or JPEG")
        return False

    print(f"  OK: {img.format} {w}x{h}, {size} bytes ({size/1024:.1f} KB)")
    return True


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(out_dir, "entry.png")

    # Create output dir if needed
    os.makedirs(out_dir, exist_ok=True)

    # Check source exists
    if not os.path.exists(SRC):
        print(f"ERROR: source file '{SRC}' not found in {os.getcwd()}")
        print(f"  Files in cwd: {[f for f in os.listdir('.') if f.endswith(('.png','.jpg','.jpeg'))]}")
        sys.exit(1)

    src_size = os.path.getsize(SRC)
    print(f"Source: {SRC} ({src_size} bytes)")

    # Copy
    import shutil
    shutil.copy2(SRC, dest)
    print(f"Copied to: {dest}")

    # Validate
    if not validate_image(dest):
        sys.exit(1)

    print("Entry ready.")


if __name__ == "__main__":
    main()
