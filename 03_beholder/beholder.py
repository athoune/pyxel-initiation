import pyxel

TRANSPARENT = 11

# Beholder states
LOADING = 0
FIRING = 1
MOVING = 2
WAITING = 3

# Hero states
HEALTHY = 0
ZAPPED = 1


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed: int
        self.angle: int  # bottom, left, right, top
        self.state: int

    def move(self, angle: int):
        # 0: don't move
        # 1: move forward
        # -1: move forward
        # angle : ↓←→↑
        self.angle = angle
        self.x += [0, -1, 1, 0][angle] * self.speed
        self.y += [1, 0, 0, -1][angle] * self.speed

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
        # Where the beholder aims
        self._aim_dx: int
        self._aim_dy: int

    def image(self):
        if self.state == LOADING:
            return self._loading_images[self.angle]
        else:
            return self._main_images[self.angle]

    def aim(self, target: Sprite):
        self.state = LOADING
        self._aim_dx = self.x - target.x
        self._aim_dy = self.y - target.y

    def shoot(self, target: Sprite):
        self.state = FIRING
        # Default values
        if self._aim_dy < 0:
            y = 0
        else:  # _aim_dy > 0
            y = pyxel.height
        if self._aim_dx < 0:
            x = 0
        else:  # _aim_dx > 0
            x = pyxel.width
        # Vertical shot exception
        if (
            self._aim_dx == 0
        ):  # the ray is 90° or 270°, /!\ division by 0 in slopee calcul
            if self._aim_dy == 0:  # Shoot on its foot
                return
            x = self.x
            xt = target.x
            yt = target.y
        else:
            slope = self._aim_dy / self._aim_dx
            if slope < 0:  # the slope has no sense, just a direction
                slope = -slope
            print("slope:", slope)
            y = slope * x
            if self._aim_dy > 0:  # the target is behind
                y = -y
            yt = self.y + (self.x - target.x + 8) * slope
            xt = self.x + (self.y - target.y + 8) / slope
        # Hit or miss
        if yt <= target.y + 8 and yt >= target.y - 8:
            target.state = ZAPPED  # side hit
        if xt <= target.x + 8 and xt >= target.x - 8:
            target.state = ZAPPED  # up (or bottom) hit
        pyxel.line(self.x + 8, self.y + 8, self.x - x, self.y + y + 8, 6)


class Hero(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 4
        self.angle = 2
        self._images = [(i * 16, 32, 16, 16, TRANSPARENT) for i in range(4)]
        self._zapped_images = [
            (64, 32, 16, 16, TRANSPARENT),
            (64, 32, -16, 16, TRANSPARENT),
        ]
        self.state = HEALTHY

    def image(self):
        if self.state == HEALTHY:
            return self._images[self.angle]
        elif self.state == ZAPPED:
            return self._zapped_images[pyxel.frame_count % 2]


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("beholder.pyxres")  # Load the assets
        self.hero = Hero(32, 104)
        self.beholder = Beholder(128, 32)
        self.game_over = 0
        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

        if self.hero.state == ZAPPED:  # Everything is frozen when the hero is zapped
            if self.game_over == 0:
                self.game_over = pyxel.frame_count
            else:
                if pyxel.frame_count - self.game_over == 30:
                    pyxel.quit()
        else:
            if pyxel.btn(pyxel.KEY_DOWN):
                self.hero.move(0)

            if pyxel.btn(pyxel.KEY_LEFT):
                self.hero.move(1)

            if pyxel.btn(pyxel.KEY_RIGHT):
                self.hero.move(2)

            if pyxel.btn(pyxel.KEY_UP):
                self.hero.move(3)

            if pyxel.frame_count % 40 == 0:  # Every 40 frames, the beholder aim
                self.beholder.aim(self.hero)

    def draw(self):
        pyxel.cls(13)  # Clear screen
        self.hero.draw()
        self.beholder.draw()
        if pyxel.frame_count % 40 == 20:
            self.beholder.shoot(self.hero)
        if self.hero.state == ZAPPED:
            pyxel.text(60, 10, "GAME OVER", 7, None)


App()
