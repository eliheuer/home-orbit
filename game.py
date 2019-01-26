import math
import random
import pyxel

SCREEN_WIDTH = 255
SCREEN_HEIGHT = 255

BUBBLE_MAX_SPEED = 0.8
BUBBLE_INITIAL_COUNT = 64
BUBBLE_EXPLODE_COUNT = 11


class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Bubble:
    def __init__(self):
        self.r = random.uniform(3, 6)

        self.pos = Vec2(
            random.uniform(self.r, SCREEN_WIDTH - self.r),
            random.uniform(self.r, SCREEN_HEIGHT - self.r),
        )

        self.vel = Vec2(
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
            random.uniform(-BUBBLE_MAX_SPEED, BUBBLE_MAX_SPEED),
        )

        self.color = 5

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        if self.vel.x < 0 and self.pos.x < self.r:
            self.vel.x *= -1

        if self.vel.x > 0 and self.pos.x > SCREEN_WIDTH - self.r:
            self.vel.x *= -1

        if self.vel.y < 0 and self.pos.y < self.r:
            self.vel.y *= -1

        if self.vel.y > 0 and self.pos.y > SCREEN_HEIGHT - self.r:
            self.vel.y *= -1


class Game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, caption="Demo Game")
        pyxel.mouse(True)
        self.is_exploded = False
        self.bubbles = [Bubble() for _ in range(BUBBLE_INITIAL_COUNT)]
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        bubble_count = len(self.bubbles)

        if pyxel.btnp(pyxel.KEY_A):
            for i in range(bubble_count):
                bubble = self.bubbles[i]
                dx = bubble.pos.x - pyxel.mouse_x
                dy = bubble.pos.y - pyxel.mouse_y

                if dx * dx + dy * dy < bubble.r * bubble.r:
                    self.is_exploded = True
                    new_r = math.sqrt(bubble.r * bubble.r / BUBBLE_EXPLODE_COUNT)

                    for j in range(BUBBLE_EXPLODE_COUNT):
                        angle = math.pi * 2 * j / BUBBLE_EXPLODE_COUNT

                        new_bubble = Bubble()
                        new_bubble.r = new_r
                        new_bubble.pos.x = bubble.pos.x + (bubble.r + new_r) * math.cos(
                            angle
                        )
                        new_bubble.pos.y = bubble.pos.y + (bubble.r + new_r) * math.sin(
                            angle
                        )
                        new_bubble.vel.x = math.cos(angle) * BUBBLE_MAX_SPEED
                        new_bubble.vel.y = math.sin(angle) * BUBBLE_MAX_SPEED
                        self.bubbles.append(new_bubble)

                    del self.bubbles[i]
                    break

        for i in range(bubble_count - 1, -1, -1):
            bi = self.bubbles[i]
            bi.update()

            for j in range(i - 1, -1, -1):
                bj = self.bubbles[j]
                dx = bi.pos.x - bj.pos.x
                dy = bi.pos.y - bj.pos.y
                total_r = bi.r + bj.r

                if dx * dx + dy * dy < total_r * total_r:
                    new_bubble = Bubble()
                    new_bubble.r = math.sqrt(bi.r * bi.r + bj.r * bj.r)
                    new_bubble.pos.x = (bi.pos.x * bi.r + bj.pos.x * bj.r) / total_r
                    new_bubble.pos.y = (bi.pos.y * bi.r + bj.pos.y * bj.r) / total_r
                    new_bubble.vel.x = (bi.vel.x * bi.r + bj.vel.x * bj.r) / total_r
                    new_bubble.vel.y = (bi.vel.y * bi.r + bj.vel.y * bj.r) / total_r
                    self.bubbles.append(new_bubble)

                    del self.bubbles[i]
                    del self.bubbles[j]
                    bubble_count -= 1
                    break

    def draw_bg(self):
        pyxel.circ(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, 32, 10)

    def draw_rings(self):
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-16, 1)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-32, 1)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-48, 1)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-64, 1)
        pyxel.circb(SCREEN_WIDTH/2, SCREEN_WIDTH/2, 128-80, 1)

    def draw_grid(self):
        for x in range(16):
            pyxel.line((x*16), 0, (x*16), 255, 1)
        for y in range(16):
            pyxel.line(0, (y*16), 255, (y*16), 1)

    def draw(self):
        pyxel.cls(0)

        self.draw_bg()
        #self.draw_grid()
        self.draw_rings()

        for bubble in self.bubbles:
            pyxel.circ(bubble.pos.x, bubble.pos.y, bubble.r, bubble.color)

        if not self.is_exploded and pyxel.frame_count % 20 < 10:
            pyxel.text(96, 50, "CLICK ON BUBBLE", pyxel.frame_count % 15 + 1)


Game()
