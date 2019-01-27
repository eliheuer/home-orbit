import pyxel
import math

SCREEN_WIDTH = 255
SCREEN_HEIGHT = 255
CENTER = 128

x_pos = 40
y_pos = 100
step = 0

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Vel:
    def __init__(self, v):
        self.v = 0.02

class Obstacle:
    def __init__(self):
        self.pos = Vec()
        self.vel = 0.01
        self.color = random.randint(1, 15)

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        self.pos.x = math.cos(self.step) * self.amp
        self.pos.y = -1 * math.sin(self.step) * self.amp
        pyxel.circ(CENTER+x_pos, CENTER+y_pos, 4, 12)
        self.step += 0.03


class Game:
    step = 0
    amp = 80
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Home Orbit")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_I):
            if self.amp <= 56:
                pass
            else:
                self.amp -= 16

        if pyxel.btnp(pyxel.KEY_O):
            if self.amp >= 112:
                pass
            else:
                self.amp += 16

    def draw(self):
        pyxel.cls(0)
        self.draw_bg()
        #self.text_time()
        self.text_life()
        #self.draw_grid()
        self.draw_rings()
        self.draw_player()

        if pyxel.btnp(pyxel.KEY_A):
            for i in range(bubble_count):
                print("A")

    def draw_player(self):
        x_pos = math.cos(self.step) * self.amp
        y_pos = -1 * math.sin(self.step) * self.amp
        pyxel.circ(CENTER+x_pos, CENTER+y_pos, 4, 12)
        self.step += 0.03

    def text_time(self):
        pyxel.text(8, 8, "Time: {}".format(pyxel.frame_count), 8)

    def text_life(self):
        pyxel.text(8, 16, "Life: {}".format(pyxel.frame_count), 7)

    def draw_bg(self):
        pyxel.circ(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 32, 10)

    def draw_rings(self):
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-16, 1)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-32, 12)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-48, 3)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-64, 9)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-80, 8)

    def draw_grid(self):
        for x in range(16):
            pyxel.line((x*16), 0, (x*16), 255, 1)
        for y in range(16):
            pyxel.line(0, (y*16), 255, (y*16), 1)


Game()
