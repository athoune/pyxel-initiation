import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="The temple")  # width, height, title
        pyxel.images[1] = pyxel.Image.from_image("temple.png", incl_colors=True)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx("temple.tmx", 0)
        pyxel.tilemaps[1].imgsrc = 1  # The map use this image for its prites

        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

    def draw(self):
        pyxel.cls(9)  # Clear screen
        # x, y, tm, u, v, w, h
        pyxel.bltm(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)


App()
