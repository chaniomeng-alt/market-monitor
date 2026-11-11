#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

BG = (13, 19, 24, 255)
HOUSING = (7, 11, 15, 255)
HOUSING_EDGE = (38, 50, 61, 255)
UP = (52, 192, 127, 255)
MID = (227, 176, 74, 255)
DOWN = (239, 106, 99, 255)

def draw_icon(size):
    img = Image.new('RGBA', (size, size), BG)
    glow = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    draw = ImageDraw.Draw(img)

    pad = size * 0.18
    hw = size * 0.38
    left = (size - hw) / 2
    right = left + hw
    top = pad
    bottom = size - pad
    radius = hw / 2

    draw.rounded_rectangle(
        [left, top, right, bottom],
        radius=radius,
        fill=HOUSING,
        outline=HOUSING_EDGE,
        width=max(1, size // 128),
    )

    inner_pad = hw * 0.28
    cy = [top + inner_pad + (bottom - top - 2 * inner_pad) * t for t in (0.0, 0.5, 1.0)]
    cx = size / 2
    lamp_r = hw * 0.28
    colors = [UP, MID, DOWN]

    for y, color in zip(cy, colors):
        glow_r = lamp_r * 1.85
        gdraw.ellipse(
            [cx - glow_r, y - glow_r, cx + glow_r, y + glow_r],
            fill=color[:3] + (70,),
        )

    glow = glow.filter(ImageFilter.GaussianBlur(radius=max(1, size * 0.03)))
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    for y, color in zip(cy, colors):
        draw.ellipse(
            [cx - lamp_r, y - lamp_r, cx + lamp_r, y + lamp_r],
            fill=color,
        )
        hr = lamp_r * 0.35
        hx = cx - lamp_r * 0.25
        hy = y - lamp_r * 0.30
        draw.ellipse(
            [hx - hr, hy - hr, hx + hr, hy + hr],
            fill=(255, 255, 255, 70),
        )

    return img.convert('RGB')

def main():
    out = Path(__file__).resolve().parents[1]
    for size, name in [(180, 'apple-touch-icon.png'), (192, 'icon-192.png'), (512, 'icon-512.png')]:
        hi = draw_icon(size * 2)
        img = hi.resize((size, size), Image.Resampling.LANCZOS)
        path = out / name
        img.save(path, 'PNG', optimize=True)
        print(f'wrote {path} {path.stat().st_size} bytes')

if __name__ == '__main__':
    main()
