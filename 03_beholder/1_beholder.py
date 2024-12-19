import pyxel

TRANSPARENT = 11


def abs(x: float) -> float:
    return x * pyxel.sgn(x)


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed: int
        self.speed = 4
        self.angle = 2
        self._images = [(i * 16, 32, 16, 16, TRANSPARENT) for i in range(4)]

    def move(self, angle: int):
        # 0: don't move
        # 1: move forward
        # -1: move forward
        # angle : ↓←→↑
        self.angle = angle
        self.x += [0, -1, 1, 0][angle] * self.speed
        self.y += [1, 0, 0, -1][angle] * self.speed
        # Can't escape the screen
        if self.x < 0:
            self.x = 0
        elif self.x > pyxel.width - 16:
            self.x = pyxel.width - 16
        if self.y < 0:
            self.y = 0
        elif self.y > pyxel.height - 16:
            self.y = pyxel.height - 16

    def image(self):
        return self._images[self.angle]

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *(self.image()))


class App:
    def __init__(self):
        pyxel.init(160, 120, title="The hero explores")  # width, height, title
        pyxel.load("beholder.pyxres")  # Load the assets
        self.hero = Hero(32, 104)
        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_DOWN):
            self.hero.move(0)
        if pyxel.btn(pyxel.KEY_LEFT):
            self.hero.move(1)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.hero.move(2)
        if pyxel.btn(pyxel.KEY_UP):
            self.hero.move(3)

    def draw(self):
        pyxel.cls(13)  # Clear screen
        self.hero.draw()


App()
