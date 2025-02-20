from typing import Iterable

import pyxel

# Color
TRANSPARENT = 0

# States
WAITING = 0
WALKING = 1
FALLING = 2
JUMP = 3
JUMPING = 4
DEAD = 5

HIT = 5
FALL = 6
GROUND = 7
OUTSIDE = 8

# Tuning
AIR_FRICTION = 0.7
FALL_SPEED = 2
JUMP_SPEED = 8
TILE_SIZE = 8
DEATH_DURATION = 60


class Sprite:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.direction: int = 1  # 1: -> -1: <-
        self.fly_direction: int = 1
        self.width = 1  # number of tile
        self.height = 1
        self.current_speed: tuple[float, float] = (0, 0)
        self.walk_speed = 2
        self.jump_speed = JUMP_SPEED
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
        "Is this a collision tile ?"
        x, y = x // TILE_SIZE, y // TILE_SIZE
        return self.collision_tilemap.pget(x, y) in self.collisions

    def move(self, who: Sprite):
        dx, dy = who.current_speed
        if who.state in (JUMP, JUMPING, FALLING) and who.fly_direction != 0:
            dx = who.fly_direction * who.walk_speed / 4
            who.fly_direction = 0

        if who.state == FALLING:
            who.current_speed = (
                who.current_speed[0] * AIR_FRICTION,
                who.current_speed[1],
            )
        elif who.state == JUMPING:
            dy = who.current_speed[1] * AIR_FRICTION
            if dy > -0.1:
                who.state = FALLING
                dy = 1
                print("Falling", dx, dy)
        elif who.state == JUMP:
            dy = -who.jump_speed
            who.state = JUMPING
        elif who.state == WALKING:
            dx = who.direction * who.walk_speed
        elif who.state == WAITING:
            dx = 0
        """
        if who.state not in (FALLING, JUMP, JUMPING):  # not FALLING nor JUMPING
            delta = who.y % TILE_SIZE
            if delta > (TILE_SIZE - 2) or delta < 2:
                who.y = (who.y // TILE_SIZE) * TILE_SIZE
        """

        target_x = who.x + dx
        target_y = who.y + dy
        if (  # The sprite can jump over the top, but not outside left, rigth, bottom sides of the screen
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
            who.state = WAITING
        if self.is_collision_tile(
            target_x, target_y + TILE_SIZE
        ) or self.is_collision_tile(target_x, target_y):  # landing
            dy = 0
            delta = who.y % TILE_SIZE
            if delta != 0:
                print("delta:", delta)
            if who.state == FALLING:
                who.state = WAITING
        if who.state not in (JUMP, JUMPING) and not self.is_collision_tile(
            target_x, target_y + TILE_SIZE + 1
        ):  # oups, falling
            who.state = FALLING
            dy = FALL_SPEED

        who.current_speed = dx, dy
        who.x += dx
        who.y += dy


class Character(Sprite):
    def update(self, world: Physics):
        if self.state == DEAD:
            if pyxel.frame_count > self.death_time:
                pyxel.quit()
            return
        direction = 0
        if pyxel.btnp(pyxel.KEY_RIGHT, 1, 1):
            direction = 1
        elif pyxel.btnp(pyxel.KEY_LEFT, 1, 1):
            direction = -1

        if self.state == WALKING and direction == 0:
            self.state = WAITING
        elif self.state in (WAITING, WALKING) and direction != 0:
            self.direction = direction
            self.state = WALKING

        if pyxel.btnp(pyxel.KEY_UP) and self.state not in (
            JUMP,
            JUMPING,
            FALLING,
        ):
            self.state = JUMP
            self.direction = direction

        if self.state in (JUMP, JUMPING, FALLING):
            self.direction = direction
            self.fly_direction = direction

        world.move(self)


class Jones(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.images_right = [(i * 8, 16, 8, 8, TRANSPARENT) for i in range(4)]
        self.images_left = [(i * 8, 16, -8, 8, TRANSPARENT) for i in range(4)]

    def image(self) -> tuple[int, int, int, int, int]:
        if self.direction == 1:
            images = self.images_right
        else:
            images = self.images_left

        if self.state == FALLING:
            return images[2]
        if self.state == WALKING:
            return images[(pyxel.frame_count // 5) % 2]  # move legs every 5 frames
        if self.state in (JUMP, JUMPING):
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
