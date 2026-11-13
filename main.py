#!/usr/bin/env python3
"""Entrypoint for ai-happy-01. Copies entry.png to output directory."""

import os
import sys
import shutil

SRC = "entry.png"


def validate_image(path: str) -> bool:
    """Validate the image meets competition constraints."""
    try:
        from PIL import Image
    except ImportError:
        print("  WARNING: PIL not available, skipping image validation")
        return True

    try:
        img = Image.open(path)
    except Exception as e:
        print(f"  FAIL: cannot open image: {e}")
        return False

    w, h = img.size
    size = os.path.getsize(path)
    fmt = img.format

    print(f"  Image: {path}")
    print(f"    Format: {fmt}")
    print(f"    Dimensions: {w}x{h}")
    print(f"    File size: {size} bytes ({size / 1024:.1f} KB)")

    ok = True
    if w > 1024 or h > 1024:
        print(f"    FAIL: dimensions {w}x{h} exceed 1024x1024")
        ok = False
    else:
        print(f"    Dimensions OK (<=1024x1024)")

    if fmt not in ("PNG", "JPEG", "JPG"):
        print(f"    FAIL: format {fmt} is not PNG or JPEG")
        ok = False
    else:
        print(f"    Format OK (PNG/JPEG)")

    if size > 1 * 1024 * 1024:
        print(f"    FAIL: file size {size} bytes exceeds 1 MiB")
        ok = False
    else:
        print(f"    Size OK (<=1 MiB)")

    return ok


def main():
    # Determine output directory
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")

    # Check source exists and is non-empty
    if not os.path.exists(SRC):
        print(f"ERROR: source image '{SRC}' not found!")
        print(f"  Run 'python3 compose.py' first to generate the entry image.")
        print(f"  Expected path: {os.path.abspath(SRC)}")
        sys.exit(1)
    if os.path.getsize(SRC) == 0:
        print(f"ERROR: source image '{SRC}' is empty (0 bytes)!")
        print(f"  Run 'python3 compose.py' again to regenerate it.")
        sys.exit(1)

    # Create output directory
    os.makedirs(out_dir, exist_ok=True)

    # Copy
    src_size = os.path.getsize(SRC)
    shutil.copy2(SRC, out_path)
    dst_size = os.path.getsize(out_path)

    print(f"Copied {SRC} ({src_size} bytes) -> {out_path} ({dst_size} bytes)")

    # Validate
    if validate_image(out_path):
        print("Validation PASSED")
    else:
        print("Validation FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()