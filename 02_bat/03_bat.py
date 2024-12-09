import pyxel


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [  # The bat uses two images : wings up, wings down
            (0, 0, 16, 16, 0),  # x, y, width, height, transparent color
            (16, 0, 16, 16, 0),
        ]
        # self.x is the top left corner of the image,
        # computing the position of the center of the bat is more intuitive
        self.center_x = self.images[0][2] / 2
        self.center_y = self.images[0][3] / 2
        self.frame = 0  # 0 : bat wings are up, 1 : down
        self.angle = 0  # Where does the bat look ?
        self.target_x: int  # The bat goes to this target
        self.target_y: int
        self.speed = 0

    def move_to(self, x, y, speed):
        "The bat rotate and will move to the target"
        self.target_x = x
        self.target_y = y
        self.speed = speed
        self.rotate_to(x, y)

    def rotate_to(self, x, y):
        self.angle = angle(x, y, self.x + self.center_x, self.y + self.center_y)

    def one_step(self):
        "The bat moves to its target"
        if self.speed != 0:
            delta = distance(
                self.target_x,
                self.target_y,
                self.x + self.center_x,
                self.y + self.center_y,
            )
            if delta <= self.speed:
                self.speed = 0
            else:
                self.x += pyxel.sin(self.angle) * self.speed
                self.y += pyxel.cos(self.angle) * self.speed

    def swap_wings(self):
        "The wings switch from up to down"
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def draw(self):
        "Draw the sprite"
        if pyxel.frame_count % 10 == 0:  # Every 10 frames, to wings swap
            self.swap_wings()
        pyxel.blt(self.x, self.y, 0, *(self.images[self.frame]))


def distance(x1, y1, x2, y2: float) -> float:
    "Euclidian distance"
    dx = x1 - x2
    dy = y1 - y2
    return pyxel.sqrt(dx**2 + dy**2)


def angle(x1, y1, x2, y2: int) -> float:
    "Get the angle between two points with trigonometry"
    dx = x1 - x2
    dy = y1 - y2
    return pyxel.atan2(dx, dy)


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("bat.pyxres")  # Load the assets

        self.bat = Bat(72, 72)  # Spawn a new bat 🦇

        pyxel.mouse(True)  # Show the mouse

        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()

        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):  # Mouse click set the target
            self.bat.move_to(pyxel.mouse_x, pyxel.mouse_y, 2)  # x, y, speed

        self.bat.one_step()  # The bat fly, one step at time

    def draw(self):
        pyxel.cls(0)  # Clear screen
        self.bat.draw()  # Draw the bat at its current position


App()
