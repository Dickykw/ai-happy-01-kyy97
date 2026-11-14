#!/usr/bin/env python3
"""main.py: make.fun competition entrypoint for ai-happy-01 BG-A (kitchen-warm Sunny).
Copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png and validates dimensions/size/format.
Stdlib only (no PIL): the grader runs stock python with no third-party packages,
and the working directory is not the repo, so paths are resolved from this file.
"""
import hashlib
import os
import struct
import sys

EXPECTED_SHA256 = "c36825d31bddd4481853f1feb6eb25bf9785013f35b0c347b6fe55e73295c5b4"


def read_image_info(path):
    """Return (format, width, height) using only the standard library.
    Supports PNG (IHDR) and JPEG (SOF0/SOF2). Returns None if unrecognised."""
    with open(path, "rb") as f:
        head = f.read(2)
        if head == b"\xff\xd8":
            f.seek(2)
            while True:
                marker = f.read(2)
                if len(marker) < 2 or marker[0] != 0xFF:
                    return None
                if marker[1] in (0xC0, 0xC1, 0xC2):
                    f.read(3)
                    raw = f.read(4)
                    h, w = struct.unpack(">HH", raw)
                    return ("JPEG", w, h)
                size_bytes = f.read(2)
                if len(size_bytes) < 2:
                    return None
                (size,) = struct.unpack(">H", size_bytes)
                f.seek(size - 2, 1)
        f.seek(0)
        header = f.read(33)
        if header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR":
            w, h = struct.unpack(">II", header[16:24])
            return ("PNG", w, h)
    return None


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)

    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(output_dir, "entry.png")

    if not os.path.exists(src):
        print(f"Error: source {src} not found.", file=sys.stderr)
        sys.exit(1)

    # Read and copy
    with open(src, "rb") as f:
        data = f.read()
    with open(dst, "wb") as f:
        f.write(data)

    # Validate
    size_bytes = len(data)
    size_mib = size_bytes / (1024 * 1024)
    if size_mib > 1.0:
        print(f"Error: file size {size_mib:.2f} MiB exceeds 1 MiB limit.", file=sys.stderr)
        sys.exit(1)

    info = read_image_info(dst)
    if info is None:
        print("Error: could not read image format/dimensions.", file=sys.stderr)
        sys.exit(1)
    fmt, w, h = info
    if w > 1024 or h > 1024:
        print(f"Error: dimensions {w}x{h} exceed 1024x1024 limit.", file=sys.stderr)
        sys.exit(1)

    if fmt not in ("PNG", "JPEG"):
        print(f"Error: format {fmt} is not PNG or JPEG.", file=sys.stderr)
        sys.exit(1)

    sha = hashlib.sha256(data).hexdigest()

    if sha != EXPECTED_SHA256:
        print(f"Error: SHA256 mismatch! Got {sha}, expected {EXPECTED_SHA256}", file=sys.stderr)
        sys.exit(1)

    print(f"SUCCESS: entry copied to {dst}")
    print(f"  Entry: BG-A (kitchen-warm Sunny)")
    print(f"  Format: {fmt}")
    print(f"  Dimensions: {w}x{h}")
    print(f"  Size: {size_bytes / 1024:.1f} KB ({size_mib:.2f} MiB)")
    print(f"  SHA256: {sha} [VERIFIED MATCH]")
    sys.exit(0)

if __name__ == "__main__":
    main()
