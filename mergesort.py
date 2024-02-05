from pyglet.window import Window
from pyglet.app import run
from pyglet.shapes import Rectangle
from pyglet.graphics import Batch
from pyglet import clock

def hex_to_rgb(hex_color):
    return int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16), 255

class Renderer(Window):
    color_tags = ["red", "green", "blue", "yellow", "purple"]

    def __init__(self):
        super().__init__(640, 640, "Merge Sort Simulation")
        self.batch = Batch()
        self.x = [3, 4, 2, 1, 5]
        self.bars = []

        self.colors = [(255, 0, 0, 255) if tag == "red" else
                       (0, 255, 0, 255) if tag == "green" else
                       (0, 0, 255, 255) if tag == "blue" else
                       (255, 255, 0, 255) if tag == "yellow" else
                       (128, 0, 128, 255) for tag in self.color_tags]

        for e, (value, color) in enumerate(zip(self.x, self.colors)):
            self.bars.append(Rectangle(100 + e * 100, 100, 80, value * 100, color=color, batch=self.batch))

        self.merge_generator = self.merge_sort_generator(self.x.copy())
        self.update_bars()

    def merge_sort_generator(self, arr):
        if len(arr) > 1:
            mid = len(arr) // 2
            left_half = arr[:mid]
            right_half = arr[mid:]

            yield left_half.copy()
            yield right_half.copy()

            yield from self.merge_sort_generator(left_half)
            yield from self.merge_sort_generator(right_half)

            i = j = k = 0

            while i < len(left_half) and j < len(right_half):
                if left_half[i] < right_half[j]:
                    arr[k] = left_half[i]
                    i += 1
                else:
                    arr[k] = right_half[j]
                    j += 1
                k += 1

            while i < len(left_half):
                arr[k] = left_half[i]
                i += 1
                k += 1

            while j < len(right_half):
                arr[k] = right_half[j]
                j += 1
                k += 1

            yield arr.copy()

    def update_bars(self):
        try:
            intermediate_state = next(self.merge_generator)
            self.bars = []

            for e, (value, color) in enumerate(zip(intermediate_state, self.colors)):
                self.bars.append(Rectangle(100 + e * 100, 100, 80, value * 100, color=color, batch=self.batch))
        except StopIteration:
            clock.unschedule(self.on_update)

    def on_update(self, deltatime):
        self.update_bars()

    def on_draw(self):
        self.clear()
        self.batch.draw()

renderer = Renderer()

clock.schedule_interval(renderer.on_update, 5)

run()
