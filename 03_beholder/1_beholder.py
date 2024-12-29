import pyxel

TRANSPARENT = 11


def between(xy: float, maxi: int) -> float:
    "The xy value is between 0 and maxi"
    if xy < 0:
        return 0
    return xy if xy < maxi else maxi


def inside_screen(x, y: float) -> tuple[float, float]:
    "The point cannot escape the screen"
    return between(x, pyxel.width - 16), between(y, pyxel.height - 16)


class Hero:
    def __init__(self, x, y):
        self.x = x
        self.y = y
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
        self.x, self.y = inside_screen(self.x, self.y)

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
