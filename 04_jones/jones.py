import pyxel

TRANSPARENT = 0

WAITING = 0
WALKING = 1
FALLING = 2
JUMPING = 3
DEAD = 4


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction = 1  # 1: -> -1: <-


class Collisions:
    def __init__(self, solids: list[tuple[int, int]]):
        "List of solids tiles"
        self.solids = solids
        self.map = 1

    def floor(self, sprite: Sprite) -> bool:
        "Does the sprite has floor under its feet?"
        if sprite.direction == -1:  # the tile before
            x = pyxel.ceil(sprite.x / 8)
        else:  # the tile after
            x = pyxel.floor(sprite.x / 8)
        # the tile under the feet of Jones
        tile = pyxel.tilemaps[self.map].pget(x, sprite.y // 8 + 1)
        return tile in self.solids

    def too_low(self, sprite: Sprite) -> bool:
        "Does the sprite fall under the bottom of the screen?"
        return sprite.y >= (pyxel.height - 8)


WORLD: Collisions


class Jones(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.images_right = [(i * 8, 16, 8, 8, TRANSPARENT) for i in range(4)]
        self.images_left = [(i * 8, 16, -8, 8, TRANSPARENT) for i in range(4)]
        self.state = WAITING
        self.how_high = 0
        self.death_time = 0

    def image(self) -> tuple[int, int, int, int, int]:
        if self.direction == 1:
            images = self.images_right
        else:
            images = self.images_left

        if self.state == FALLING:
            return images[2]
        if self.state == WALKING:
            return images[(pyxel.frame_count // 5) % 2]  # move legs every 5 frames
        if self.state == JUMPING:
            return images[3]
        # WAITING
        return images[0]

    def physic(self):
        if self.state == DEAD:  # there is no physics when you are a soul
            return
        if self.state == JUMPING:
            if self.y > self.how_high:
                self.y -= 2
                self.x += self.direction
            else:  # start falling soon
                self.state = WAITING
            return
        if WORLD.too_low(self):
            self.death_time = pyxel.frame_count + 30
            self.state = DEAD
            return
        if WORLD.floor(self):
            if self.state == FALLING:
                self.state = WAITING  # soft landing
            return
        else:
            self.state = FALLING
            self.y += 2

    def move(self, direction):
        if direction == 0:
            self.state = WAITING
        else:
            self.state = WALKING
            self.direction = direction
            self.x += self.direction * 2

    def jump(self, direction):
        self.state = JUMPING
        self.how_high = self.y - 16
        self.direction = direction

    def update(self):
        if self.state in (WAITING, WALKING):
            if pyxel.btn(pyxel.KEY_RIGHT):
                dx = 1
            elif pyxel.btn(pyxel.KEY_LEFT):
                dx = -1
            else:
                dx = 0

            if pyxel.btnp(pyxel.KEY_UP):
                self.jump(dx)
            else:
                self.move(dx)
        if self.state == DEAD and pyxel.frame_count > self.death_time:
            pyxel.quit()
        self.physic()

    def draw(self):
        if self.state == DEAD:
            if pyxel.frame_count % 10 < 5:
                pyxel.text(70, 10, "GAME OVER", 8, None)
        else:
            pyxel.blt(self.x, self.y, 1, *(self.image()))


class App:
    def __init__(self):
        pyxel.init(160, 120, title="The temple")  # width, height, title
        pyxel.images[1] = pyxel.Image.from_image("temple.png", incl_colors=True)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx("temple.tmx", 0)
        pyxel.tilemaps[1].imgsrc = 1  # The map use this image for its prites

        global WORLD
        WORLD = Collisions([(0, 0), (1, 0), (2, 0)])

        self.jones = Jones(8, 0)

        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()
        self.jones.update()

    def draw(self):
        pyxel.cls(9)  # Clear screen
        # x, y, tm, u, v, w, h
        pyxel.bltm(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)
        self.jones.draw()


App()
