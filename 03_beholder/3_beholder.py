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


def abs(x: float) -> float:
    return x * pyxel.sgn(x)


def between(xy: float, maxi: int) -> float:
    "The xy value is between 0 and maxi"
    if xy < 0:
        return 0
    return xy if xy < maxi else maxi


def inside_screen(x, y: float) -> tuple[float, float]:
    "The point cannot escape the screen"
    return between(x, pyxel.width - 16), between(y, pyxel.height - 16)


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
        # Can't escape the screen
        self.x, self.y = inside_screen(self.x, self.y)

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

    def watch(self, target: Sprite):
        dx, dy = self.x - target.x, self.y - target.y
        if abs(dx) > abs(dy):
            self.angle = 1 if dx > 0 else 2
        else:
            self.angle = 3 if dy > 0 else 0

    def aim(self, target: Sprite):
        self.state = LOADING
        self._aim_dx, self._aim_dy = self.x - target.x, self.y - target.y

    def shoot(self, target: Sprite):
        self.state = FIRING
        # The ray starts avec self.x, self.y
        x_end: float  # horizontal end of the ray
        y_end: float  # vertical end of the ray

        # Center of the shooter
        shooter_x, shooter_y = self.x + 8, self.y + 8
        # Center of the target
        target_x, target_y = target.x + 8, target.y + 8
        # Side hit by the shot
        target_side_x = target_x + pyxel.sgn(self._aim_dx) * 8
        target_side_y = target_y + pyxel.sgn(self._aim_dy) * 8

        # Where the ray ends when it miss ?

        cross = [  # x, y
            [(pyxel.width, pyxel.height), (pyxel.width, shooter_y), (pyxel.width, 0)],
            [(shooter_x, pyxel.height), (None, None), (shooter_x, 0)],
            [(0, pyxel.height), (0, shooter_y), (0, 0)],
        ]
        x_end, y_end = cross[pyxel.sgn(self._aim_dx) + 1][pyxel.sgn(self._aim_dy) + 1]

        if x_end is None:  # It shots its own foot
            return

        x_hit, y_hit = shooter_x, shooter_y
        if self._aim_dx != 0:
            slope = self._aim_dy / self._aim_dx
            y_end = (x_end - shooter_x) * slope + shooter_y
            y_hit = (target_side_x - shooter_x) * slope + shooter_y
            if slope != 0:
                x_end = (y_end - shooter_y) / slope + shooter_x
                x_hit = (target_side_y - shooter_y) / slope + shooter_x
        if abs(target_x - x_hit) <= 8:
            x_end, y_end = x_hit, target_side_y
            target.state = ZAPPED
        if abs(target_y - y_hit) <= 8:
            x_end, y_end = target_side_x, y_hit
            target.state = ZAPPED
        bolt_color = 10 if target.state == ZAPPED else 6
        pyxel.line(shooter_x, shooter_y, x_end, y_end, bolt_color)


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
        # width, height, title
        pyxel.init(160, 120, title="The beholder and its beam of death")
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

            self.beholder.watch(self.hero)
            if pyxel.frame_count % 40 == 10:  # Every 50 frames, the beholder aim
                self.beholder.aim(self.hero)
            if pyxel.frame_count % 40 == 30:  # 25 later, it shoots
                self.beholder.state = FIRING

    def draw(self):
        pyxel.cls(13)  # Clear screen
        self.hero.draw()
        if self.beholder.state == FIRING:
            self.beholder.shoot(self.hero)
        self.beholder.draw()
        if self.hero.state == ZAPPED:
            pyxel.text(60, 10, "GAME OVER", 7, None)


App()
