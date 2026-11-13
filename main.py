#!/usr/bin/env python3
"""
Entrypoint for ai-happy-01 (make.fun competition).
Copies entry.png to the output directory, validates it,
and reports results.
"""

import os
import shutil
import sys
from PIL import Image

SRC = "entry.png"


def validate(path: str) -> tuple[bool, str]:
    """Check that the image meets competition rules."""
    try:
        img = Image.open(path)
    except Exception as e:
        return False, f"Cannot open image: {e}"

    fmt = img.format
    w, h = img.size
    size = os.path.getsize(path)

    if fmt not in ("PNG", "JPEG", "JPG"):
        return False, f"Format must be PNG or JPEG, got {fmt}"

    if w > 1024 or h > 1024:
        return False, f"Dimensions {w}x{h} exceed 1024x1024"

    if size > 1_048_576:
        return False, f"File size {size} bytes exceeds 1 MiB limit"

    return True, f"Valid: {fmt} {w}x{h} {size} bytes"


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    dest = os.path.join(output_dir, "entry.png")

    os.makedirs(output_dir, exist_ok=True)

    if not os.path.isfile(SRC):
        print(f"ERROR: {SRC} not found. Run compose.py first.")
        sys.exit(1)

    src_size = os.path.getsize(SRC)
    shutil.copy2(SRC, dest)
    dst_size = os.path.getsize(dest)

    print(f"Copied {SRC} ({src_size} bytes) -> {dest} ({dst_size} bytes)")

    ok, msg = validate(dest)
    print(f"Validation: {msg}")
    if not ok:
        sys.exit(1)

    # Show a quick preview summary
    img = Image.open(dest)
    print(f"Preview: {img.size[0]}x{img.size[1]} {img.format}, "
          f"{dst_size / 1024:.1f} KB — ready for submission.")
    img.close()

    print("Entry is ready.")


if __name__ == "__main__":
    main()
