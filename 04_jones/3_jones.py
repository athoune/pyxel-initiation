from typing import Iterable

import pyxel

# Color
TRANSPARENT = 0

# States
WAITING = 0
WALKING = 1
FALLING = 2
JUMPING = 3
DEAD = 4

HIT = 5
FALL = 6
GROUND = 7
OUTSIDE = 8

# Tuning
AIR_FRICTION = 0.8
GRAVITY = 0.2
FALL_SPEED = 2
JUMP_SPEED = 6
TILE_SIZE = 8
DEATH_DURATION = 60


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction: int = 1  # 1: -> -1: <-
        self.width = 1  # number of tile
        self.height = 1
        self.current_speed: tuple[int, int] = (0, 0)
        self.walk_speed = 2
        self.jump_speed = 1
        self.state = WAITING
        self.death_time = 0


class Physics:
    def __init__(
        self, collision_tiles: Iterable[tuple[int, int]], collision_tilemap: int
    ):
        # list of solid tiles
        self.collisions = frozenset(collision_tiles)
        self.collision_tilemap = pyxel.tilemaps[collision_tilemap]

    def is_collision_tile(self, x, y):
        x, y = x // TILE_SIZE, y // TILE_SIZE
        return self.collision_tilemap.pget(x, y) in self.collisions

    def goto(self, who: Sprite, dx: float, dy: float):
        if who.state == FALLING:
            dy = who.current_speed[1]
        elif who.state == JUMPING:
            dx = who.current_speed[0]
            dy = who.current_speed[1] * AIR_FRICTION
            if dy > -0.1:
                dy = FALL_SPEED / 4
                print("Falling", dx, dy)
        else:  # not FALLING nor JUMPING
            if (who.y % TILE_SIZE) > (TILE_SIZE - 1):
                who.y = (who.y // TILE_SIZE) * TILE_SIZE

        target_x = who.x + dx
        target_y = who.y + dy
        if (  # The sprite can jump outside
            target_x < 0
            or target_x > pyxel.width + TILE_SIZE
            or target_y >= pyxel.height - TILE_SIZE
        ):
            who.state = DEAD
            who.death_time = pyxel.frame_count + DEATH_DURATION
            return

        if dy < 0 and self.is_collision_tile(target_x, target_y):  # bim, the ceil
            dy = 0
        if (dx > 0 and self.is_collision_tile(target_x + TILE_SIZE, target_y)) or (
            dx < 0 and self.is_collision_tile(target_x, target_y)
        ):  # bim, the wall
            dx = 0
        if self.is_collision_tile(target_x, target_y + TILE_SIZE):  # landing
            dy = 0
            if who.state == FALLING:
                who.state = WAITING
        if not self.is_collision_tile(
            target_x, target_y + TILE_SIZE + 1
        ):  # oups, falling
            dy += FALL_SPEED

        if dx == 0 and dy == 0:
            who.state = WAITING
        elif dx != 0:
            who.state = WALKING
            who.direction = pyxel.sgn(dx)
        elif dy < 0:
            who.state = JUMPING
        elif dy > 0:
            who.state = FALLING

        who.current_speed = dx, dy
        who.x += dx
        who.y += dy
        print(
            "state",
            who.state,
            "d (",
            dx,
            dy,
            ") who(",
            who.x,
            who.y,
            ")",
            who.y % TILE_SIZE,
        )


class Character(Sprite):
    def update(self, world: Physics):
        if self.state == DEAD:
            if pyxel.frame_count > self.death_time:
                pyxel.quit()
            return
        dx, dy = 0, 0
        if self.state in (WAITING, WALKING, JUMPING):
            if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
                dx = self.walk_speed
            elif pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
                dx = -self.walk_speed
            if pyxel.btnp(pyxel.KEY_UP, 1, 1) and self.state != JUMPING:
                dy = -JUMP_SPEED
        world.goto(self, dx, dy)


class Jones(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.images_right = [(i * 8, 16, 8, 8, TRANSPARENT) for i in range(4)]
        self.images_left = [(i * 8, 16, -8, 8, TRANSPARENT) for i in range(4)]
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

    def draw(self):
        if self.state == DEAD:
            if pyxel.frame_count % 10 < 5:
                pyxel.text(70, 10, "GAME OVER", 8, None)
        else:
            pyxel.blt(self.x, self.y, 1, *(self.image()))


class App:
    def __init__(self):
        pyxel.init(160, 120, title="The temple", fps=30)  # width, height, title
        pyxel.images[1] = pyxel.Image.from_image("temple.png", incl_colors=True)
        pyxel.tilemaps[1] = pyxel.Tilemap.from_tmx("temple.tmx", 0)
        pyxel.tilemaps[1].imgsrc = 1  # The map use this image for its prites

        self.world = Physics([(0, 0), (1, 0), (2, 0)], 1)

        self.jones = Jones(8, 0)

        pyxel.run(self.update, self.draw)  # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):  # Hit Q to quit
            pyxel.quit()
        self.jones.update(self.world)

    def draw(self):
        pyxel.cls(9)  # Clear screen
        # x, y, tm, u, v, w, h
        pyxel.bltm(0, 0, 1, 0, 0, pyxel.width, pyxel.height, 0)
        self.jones.draw()


App()
