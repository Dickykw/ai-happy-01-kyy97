# ai-happy-01 — Shelby the Turtle 🐢🌼

A warm storybook scene for the AI judge: a handwritten letter from a tiny
turtle named Shelby, who walked three weeks to bring the judge a real flower.

**What's in the image:**
- Top: a piece of lined paper taped to a wooden wall, with a handwritten
  letter (Caveat font) from Shelby to the judge.
- Bottom: a wooden desk with a polaroid-style photo of Shelby the turtle
  (generated via Pollinations.ai FLUX), holding a tiny yellow daisy.

**How it was made:**
- The turtle illustration was generated with Pollinations.ai (FLUX model,
  seed 44) using a prompt for a cute cartoon baby turtle with a daisy.
- The letter text is rendered with the Caveat handwriting font.
- The composition (wood textures, paper, tape, polaroid frame, warm
  lighting, vignette) is built with Python PIL.

**Files:**
- `main.py` — entrypoint, copies `entry.png` to the output directory.
- `compose.py` — generates `entry.png` (1024x1024, ~345 KB).
- `gen_image.py` — fetches turtle candidates from Pollinations API.
- `draw_turtle.py` — PIL-only turtle drawing (unused in final, kept as fallback).
- `entry.png` — the final image.
- `Caveat.ttf` — handwriting font for the letter.
- `cand2-44.jpg` — the winning Pollinations turtle illustration.
- `LICENSE` — MIT License.
- `.makefun/owner.json` — wallet address.

**Entry:** `main.py` → copies `entry.png` to `/output/entry.png`.