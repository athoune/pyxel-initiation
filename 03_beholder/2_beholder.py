import pyxel

TRANSPARENT = 11
# Beholder states
LOADING = 0
WAITING = 3


def abs(x: float) -> float:
    return x * pyxel.sgn(x)


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed: int
        self.angle: int  # bottom, left, right, top

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

    def image(self) -> tuple[int, int, int, int, int]:
        # What is the current image
        raise NotImplementedError

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *(self.image()))


class Beholder(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.angle = 1
        self.speed = 2
        self.state = WAITING
        # The beholder can be normal : waiting, aiming, moving…
        self._main_images = [(i * 16, 0, 16, 16, TRANSPARENT) for i in range(4)]
        # The beholder loads its death ray
        self._loading_images = [(i * 16, 16, 16, 16, TRANSPARENT) for i in range(4)]

    def watch(self, target: Sprite):
        dx, dy = self.x - target.x, self.y - target.y
        if abs(dx) > abs(dy):
            self.angle = 1 if dx > 0 else 2
        else:
            self.angle = 3 if dy > 0 else 0

    def image(self):
        if self.state == LOADING:
            return self._loading_images[self.angle]
        else:
            return self._main_images[self.angle]


class Hero(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 4
        self.angle = 2
        self._images = [(i * 16, 32, 16, 16, TRANSPARENT) for i in range(4)]

    def image(self):
        return self._images[self.angle]


class App:
    def __init__(self):
        # width, height, title
        pyxel.init(160, 120, title="The beholder watch the hero")
        pyxel.load("beholder.pyxres")  # Load the assets
        self.hero = Hero(32, 104)
        self.beholder = Beholder(128, 32)
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

        if pyxel.btn(pyxel.KEY_SPACE):
            self.beholder.state = LOADING
        else:
            self.beholder.state = WAITING
        self.beholder.watch(self.hero)

    def draw(self):
        pyxel.cls(13)  # Clear screen
        self.hero.draw()
        self.beholder.draw()


App()
