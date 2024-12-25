#!/usr/bin/env python3

"""
Piskel square output is painful, one long column is easier to use.
https://www.piskelapp.com/
"""

from PIL import Image

SIZE = 16


def columnize(img: Image.Image) -> Image.Image:
    width = int(img.size[0] / SIZE)
    height = int(img.size[1] / SIZE)

    not_empty = 0  # Number of not emptye sprites
    for line in range(height):
        for column in range(width):
            first = img.getpixel((line, column))
            ok = True

            for i in range(SIZE):
                for j in range(SIZE):
                    p = img.getpixel((j + column * SIZE, i + line * SIZE))
                    if p != first:
                        ok = False
            if not ok:
                not_empty = not_empty + 1

    out = Image.new("RGBA", (SIZE, not_empty * SIZE))
    i = 0
    for line in range(height):
        for column in range(width):
            # left, upper, right, lower
            thumb = img.crop(
                (column * SIZE, line * SIZE, (column + 1) * SIZE, (line + 1) * SIZE)
            )
            out.paste(thumb, (0, i * SIZE))
            i = i + 1
    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) == 1:
        print("I nedd some png paths as arguments")
    else:
        for square in sys.argv[1:]:
            square = Path(square)
            img = Image.open(square)
            out = columnize(img)
            out.save(square.stem + "_col" + square.suffixes[0])
            print("✓", square)
