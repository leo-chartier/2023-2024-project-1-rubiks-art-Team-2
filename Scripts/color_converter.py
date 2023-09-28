from math import floor, sqrt
from PIL import Image, UnidentifiedImageError
from PIL.ImagePalette import ImagePalette
import os

COLORS = [
    0xFFFFFF, # white
    0xFFFF00, # yellow
    0x0080FF, # blue
    0x00C000, # green
    0xFF0000, # red
    0xFF8000, # orange
]

def resize(img: Image.Image, name: str) -> Image.Image:
    MAX_CUBES = 3000

    # w, h: Size in cubes
    # W, H: Size in cubies/pixels (3x size in cubes)

    # w * h <= MAX_CUBES
    # w / h = W / H ~= aspect_ratio = img.width / img.height

    # => w = aspect_ratio * h
    # => (aspect_ratio * h) * h <= MAX_CUBES
    # => h <= sqrt(MAX_CUBES / aspect_ratio)

    aspect_ratio = img.width / img.height

    h = floor(sqrt(MAX_CUBES / aspect_ratio))
    w = round(aspect_ratio * h)
    W, H = w * 3, h * 3

    print(f"{name}: {w * h} cubes for a {W}x{H} image")

    scale = min(img.width / W, img.height / H)
    new = Image.new(img.mode, (W, H))
    new.paste(img.resize((int(img.width / scale), int(img.height / scale))))
    return new

def convert_colors(img: Image.Image) -> Image.Image:
    palette = ImagePalette("RGB", palette=bytearray(
        (color >> i) & 0xFF
        for color in COLORS
        for i in range(16, -1, -8)
    ))
    quantize_img = Image.new("P", img.size)
    quantize_img.putpalette(palette)
    return img.convert("RGB").quantize(palette=quantize_img, method=Image.Quantize.MAXCOVERAGE)

def main():
    base_path = r"[REDACTED]"
    for fn in os.listdir(base_path):
        path = os.path.join(base_path, fn)
        try:
            original = Image.open(path).convert("RGB")
        except UnidentifiedImageError:
            continue
        img = convert_colors(resize(original, fn))
        save_base = r"[REDACTED]"
        os.makedirs(save_base, exist_ok=True)
        save_path = os.path.join(save_base, os.path.splitext(os.path.basename(path))[0] + ".png")
        img.convert("RGB").save(save_path)

if __name__ == "__main__":
    main()
