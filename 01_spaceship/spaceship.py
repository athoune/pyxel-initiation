"""
Explore the galaxy with an alien spaceship.

Minimalistic Pyxel example
"""

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="UFO exploration")  # width, height, title
        pyxel.load("spaceship.pyxres")
        self.player_x = 72  # 🛸 X position
        self.player_y = 72  # 🛸 Y position
        self.spaceship_r = (0, 0, 16, 16, 0)  # x, y, width, height, transparent color
        self.spaceship_l = (16, 0, 16, 16, 0)
        self.ship = self.spaceship_r  # 🛸 looks ->

        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)  # go ->
            self.ship = self.spaceship_l  # 🛸 looks <-
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)  # go ->
            self.ship = self.spaceship_r  # 🛸 looks ->
        # 🛸 bumps slowly 1/16 per tick starting with y = 72
        self.player_y = pyxel.cos(pyxel.frame_count * 360 / 16) + 72

    def draw(self):
        pyxel.cls(0)  # clear screen with color 0

        # Draw 🛸
        pyxel.blt(self.player_x, self.player_y, 0, *self.ship)


App()
