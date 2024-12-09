import pyxel


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [
            (0, 0, 16, 16, 0),  # x, y, width, height, transparent color
            (16, 0, 16, 16, 0),
        ]
        self.step = 0

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *(self.images[self.step]))

    def flip(self):
        if self.step == 0:
            self.step = 1
        else:
            self.step = 0


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("bat.pyxres")

        self.bat = Bat(72, 72)

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.frame_count % 10 == 0:
            self.bat.flip()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.bat.x = pyxel.mouse_x
            self.bat.y = pyxel.mouse_y
            pyxel.mouse(False)
        else:
            pyxel.mouse(True)

    def draw(self):
        pyxel.cls(0)

        self.bat.draw()


App()
