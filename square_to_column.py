#!/usr/bin/env python3

"""
Piskel square output is painful, one long column is easier to use.
https://www.piskelapp.com/
"""

from PIL import Image

SIZE = 16

img = Image.open("bobby.png")
print(img.size)

width = int(img.size[0] / SIZE)
height = int(img.size[1] / SIZE)

not_empty = 0
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
        print(line, column, ok)
print(not_empty)

frames = img.size[0] / SIZE * img.size[1] / SIZE
out = Image.new("RGBA", (SIZE, not_empty * SIZE))
# left, upper, right, lower
i = 0
for line in range(height):
    for column in range(width):
        thumb = img.crop(
            (column * SIZE, line * SIZE, (column + 1) * SIZE, (line + 1) * SIZE)
        )
        out.paste(thumb, (0, i * SIZE))
        i = i + 1
out.save("out.png")
