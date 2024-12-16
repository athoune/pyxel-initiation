import pyxel

TRANSPARENT = 11

LOADING = 0
FIRING = 1
MOVING = 2
WAITING = 3


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed: int
        self.angle: int  # bottom, left, right, top
        self._images = []

    def move(self):
        d = [(0, 1), (-1, 0), (1, 0), (0, -1)][self.angle]
        self.x += d[0] * self.speed
        self.y += d[1] * self.speed

    def image(self) -> tuple:
        raise NotImplementedError

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *(self.image()))


class Beholder(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.angle = 1
        self.speed = 2
        self.state = WAITING
        self._main_images = [(i * 16, 0, 16, 16, TRANSPARENT) for i in range(4)]
        self._loading_images = [(i * 16, 16, 16, 16, TRANSPARENT) for i in range(4)]
        self._aim_dx: int
        self._aim_dy: int

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
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("beholder.pyxres")  # Load the assets
        self.hero = Hero(32, 104)
        self.beholder = Beholder(128, 32)
        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_DOWN):
            self.hero.angle = 0
            self.hero.move()

        if pyxel.btn(pyxel.KEY_LEFT):
            self.hero.angle = 1
            self.hero.move()

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.hero.angle = 2
            self.hero.move()

        if pyxel.btn(pyxel.KEY_UP):
            self.hero.angle = 3
            self.hero.move()

        if pyxel.frame_count % 40 == 0:
            self.beholder.aim(self.hero)

    def draw(self):
        pyxel.cls(13)  # Clear screen
        self.hero.draw()
        self.beholder.draw()

App()
