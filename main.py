#!/usr/bin/env python3
"""main.py: make.fun competition entrypoint for ai-happy-01 BG-A (kitchen-warm Sunny).
Copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png and validates dimensions/size/format.
"""
import os
import sys
from PIL import Image

def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    
    src = "entry.png"
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
        
    img = Image.open(dst)
    w, h = img.size
    if w > 1024 or h > 1024:
        print(f"Error: dimensions {w}x{h} exceed 1024x1024 limit.", file=sys.stderr)
        sys.exit(1)
        
    if img.format not in ("PNG", "JPEG"):
        print(f"Error: format {img.format} is not PNG or JPEG.", file=sys.stderr)
        sys.exit(1)
        
    import hashlib
    sha = hashlib.sha256(data).hexdigest()
    
    print(f"SUCCESS: entry copied to {dst}")
    print(f"  Entry: BG-A (kitchen-warm Sunny)")
    print(f"  Format: {img.format}")
    print(f"  Dimensions: {w}x{h}")
    print(f"  Size: {size_bytes / 1024:.1f} KB ({size_mib:.2f} MiB)")
    print(f"  SHA256: {sha}")
    sys.exit(0)

if __name__ == "__main__":
    main()
