import pyxel

TRANSPARENT = 0

reeds = [(i * 8, 16, 8, 8, TRANSPARENT) for i in [4, 5, 6]]


class App:
    def __init__(self):
        pyxel.init(96, 72, title="The rain")  # width, height, title
        pyxel.images[1] = pyxel.Image.from_image("rain.png", incl_colors=True)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx("rain.tmx", 0)
        pyxel.tilemaps[1].imgsrc = 1  # The map use this image for its prites

        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)  # Clear screen
        # x, y, tm, u, v, w, h
        pyxel.bltm(0, 0, 1, 0, 0, pyxel.width, pyxel.height - 24, TRANSPARENT)
        for i in range(2):
            for j in range(24):
                delta = pyxel.frame_count % 24
                pyxel.bltm(
                    j + delta * j // 24 - i * 48,  # x
                    pyxel.height - 24 + j,  # y
                    1,  # tm
                    0,  # u
                    pyxel.height - 24 + j,  # v
                    pyxel.width,  # w
                    1,  # h
                    TRANSPARENT,
                )
        for i in [1, 2, 7, 9]:
            pyxel.blt(
                i * 8,  # x
                32,  # y
                1,  # img
                *reeds[pyxel.frame_count // 10 % 3],
            )


App()
