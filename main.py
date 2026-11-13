#!/usr/bin/env python3
"""
Entrypoint for ai-happy-01 (make.fun competition).
Copies the composed entry.png to $MAKEFUN_OUTPUT_DIR (or /output/entry.png)
and validates the copied file: size <= 1 MiB, dimensions <= 1024x1024,
format PNG or JPEG.
"""

import os
import shutil
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    Image = None

SOURCE = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"
MAX_BYTES = 1 * 1024 * 1024  # 1 MiB
MAX_DIM = 1024
ALLOWED_FORMATS = {"PNG", "JPEG"}


def validate(path: Path):
    """Return a list of problems; empty list means the output is valid."""
    problems = []

    size = path.stat().st_size
    if size > MAX_BYTES:
        problems.append(
            f"too large: {size:,} bytes > {MAX_BYTES:,} bytes (1 MiB)"
        )

    if Image is None:
        problems.append("PIL not installed - cannot verify dimensions/format")
        return problems

    try:
        with Image.open(path) as img:
            w, h = img.size
            fmt = (img.format or "").upper()
            if w > MAX_DIM or h > MAX_DIM:
                problems.append(
                    f"dimensions {w}x{h} exceed {MAX_DIM}x{MAX_DIM}"
                )
            if fmt not in ALLOWED_FORMATS:
                problems.append(f"format {fmt} not in {ALLOWED_FORMATS}")
    except Exception as exc:  # corrupt/truncated file
        problems.append(f"cannot open as image: {exc}")

    return problems


def main():
    # ---- resolve source ----
    src = Path(__file__).resolve().parent / SOURCE
    if not src.exists():
        print(f"ERROR: source image not found: {src}")
        print("Run compose.py first to generate entry.png.")
        sys.exit(1)

    # Validate the source *before* copying, so a stale or broken
    # entry.png can never silently reach the output directory.
    src_problems = validate(src)
    if src_problems:
        print(f"ERROR: source image {src} is not usable:")
        for p in src_problems:
            print(f"  - {p}")
        print("Re-run compose.py to regenerate entry.png.")
        sys.exit(1)
    print(f"Source image OK: {src}")

    # ---- resolve destination dir ----
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / SOURCE

    # ---- copy ----
    shutil.copy2(src, dest)
    print(f"Copied {src} -> {dest}")
    print(f"  source size: {src.stat().st_size:,} bytes")
    print(f"  dest   size: {dest.stat().st_size:,} bytes")

    # ---- validate copied output ----
    problems = validate(dest)
    if problems:
        print("VALIDATION FAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    if Image is not None:
        with Image.open(dest) as img:
            print(
                f"VALIDATION OK: {img.format} "
                f"{img.size[0]}x{img.size[1]}, "
                f"{dest.stat().st_size:,} bytes (<= 1 MiB)"
            )
    else:
        print("VALIDATION OK: size within limits (PIL unavailable, "
              "dimensions/format not checked)")


if __name__ == "__main__":
    main()