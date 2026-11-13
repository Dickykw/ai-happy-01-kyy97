#!/usr/bin/env python3
"""
Entrypoint for ai-happy-01.
Copies entry.png to the output directory and validates it.
"""

import os
import shutil
import sys
from PIL import Image

SRC = "entry.png"


def validate(path: str) -> bool:
    """Validate that the output file meets all constraints."""
    try:
        size = os.path.getsize(path)
        img = Image.open(path)
        w, h = img.size
        fmt = img.format
    except Exception as e:
        print(f"  VALIDATION FAILED: {e}")
        return False

    checks = []
    # Max 1 MiB
    size_ok = size <= 1_048_576
    checks.append(("size ≤ 1 MiB", f"{size/1024:.1f} KB", size_ok))
    # Max 1024x1024
    dim_ok = w <= 1024 and h <= 1024
    checks.append(("dimensions ≤ 1024x1024", f"{w}x{h}", dim_ok))
    # Must be PNG or JPEG
    fmt_ok = fmt in ("PNG", "JPEG", "JPG")
    checks.append(("format PNG/JPEG", str(fmt), fmt_ok))

    all_ok = True
    for label, value, passed in checks:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] {label}: {value}")
        if not passed:
            all_ok = False

    return all_ok


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(SRC):
        print(f"ERROR: source file '{SRC}' not found in {os.getcwd()}")
        sys.exit(1)

    src_size = os.path.getsize(SRC)
    shutil.copy2(SRC, dst)
    dst_size = os.path.getsize(dst)

    print(f"Copied {SRC} ({src_size} bytes) -> {dst} ({dst_size} bytes)")

    if not validate(dst):
        sys.exit(1)

    print("Done.")


if __name__ == "__main__":
    main()