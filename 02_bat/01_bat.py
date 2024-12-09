import pyxel


class Bat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.images = [ # The bat uses two images : wings up, wings down
            (0, 0, 16, 16, 0),  # x, y, width, height, transparent color
            (16, 0, 16, 16, 0),
        ]
        self.frame = 0 # 0 : bat wings are up, 1 : down

    def flip(self):
        "The wings switch from up to dwon"
        if self.frame == 0:
            self.frame = 1
        else:
            self.frame = 0

    def draw(self):
        "Draw the sprite"
        if pyxel.frame_count % 10 == 0: # Every 10 frames, to wings flip
            self.flip()
        pyxel.blt(self.x, self.y, 0, *(self.images[self.frame]))


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Flying bat")  # width, height, title
        pyxel.load("bat.pyxres") # Load the assets

        self.bat = Bat(72, 72) # Spawn a new bat 🦇

        pyxel.run(self.update, self.draw) # Starts Pyxel loop

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): # Hit Q to quit
            pyxel.quit()

    def draw(self):
        pyxel.cls(0) # Clear screen
        self.bat.draw() # Draw the bat at its current position


App()
