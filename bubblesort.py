from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock
import random

class Renderer(Window):
    def __init__(self):
        super().__init__(640, 640, "Bubble Sort Simulation")
        self.batch = Batch()
        self.x = [3, 4, 2, 1, 5]
        self.bars = []

        self.color_tags = ["red", "green", "blue", "yellow", "purple"]

        self.colors = [(255, 0, 0, 255) if tag == "red" else
                       (0, 255, 0, 255) if tag == "green" else
                       (0, 0, 255, 255) if tag == "blue" else
                       (255, 255, 0, 255) if tag == "yellow" else
                       (128, 0, 128, 255) for tag in self.color_tags]

        for e, i in enumerate(self.x):
            self.bars.append(Rectangle(100 + e * 100, 100, 80, i * 100, color=self.colors[e], batch=self.batch))

    def on_update(self, deltatime):
        n = len(self.x)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if self.x[j] > self.x[j + 1]:
                    self.x[j], self.x[j + 1] = self.x[j + 1], self.x[j]

                    for e, i in enumerate(self.x):
                        self.bars[e].position = 100 + e * 100, 100
                        self.bars[e].height = i * 100
                    return

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()
clock.schedule_interval(renderer.on_update, 3)
run()