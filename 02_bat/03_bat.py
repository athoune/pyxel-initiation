import pyxel


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [
            (0, 0, 16, 16, 0),  # x, y, width, height, transparent color
            (16, 0, 16, 16, 0),
        ]
        self.width = self.images[0][2]
        self.height = self.images[0][3]
        self.step = 0
        self.angle = 0
        self.target_x: int
        self.target_y: int
        self.moving = False

    def draw(self):
        pyxel.blt(self.x, self.y, 0, *(self.images[self.step]))

    def flip(self):
        if self.step == 0:
            self.step = 1
        else:
            self.step = 0

    def one_step(self, step: float):
        if self.moving:
            delta = distance(self.target_x,
                             self.target_y,
                             self.x,
                             self.y)
            if delta <= step:
                self.moving = False
            else:
                self.x += pyxel.sin(self.angle) * step
                self.y += pyxel.cos(self.angle) * step

    def move_to(self, x, y):
        self.target_x = x
        self.target_y = y
        self.rotate_to(x, y)
        self.moving = True

    def rotate_to(self, x, y):
        self.angle = angle(x, y, self.x, self.y)


def distance(x1, y1, x2, y2: int) -> float:
    dx = x1 - x2
    dy = y1 - y2
    return pyxel.sqrt(dx**2 + dy**2)


def angle(x1, y1, x2, y2: int) -> float:
    dx = x1 - x2
    dy = y1 - y2
    return pyxel.atan2(dx, dy)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("bat.pyxres")

        self.bat = Bat(72, 72)
        self.angle = -1.0

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.frame_count % 10 == 0:
            self.bat.flip()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            self.bat.move_to(pyxel.mouse_x, pyxel.mouse_y)

        SPEED = 2
        self.bat.one_step(SPEED)

    def draw(self):
        pyxel.cls(0)

        self.bat.draw()


App()
