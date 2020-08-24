from PIL import Image, ImageDraw
import numpy as np
import math
import time
import os


class DrawMaster:
    def __init__(self, name="DrawMaster",
                 size=(100, 100), background=(150, 130, 200)):
        self.name = name
        self.width, self.height = size
        self.picture = Image.new(
            'RGB', (self.width, self.height), background)
        self.draw = ImageDraw.Draw(self.picture)
        self.center = (self.width//2, self.height//2)

    def checkerboard(self, blockSize=1):
        if self.width % blockSize != 0 \
                or self.height % blockSize != 0:
            raise ValueError('Block size will not fit image')
        cols = self.width // blockSize
        rows = self.height // blockSize
        row_color = [0, 0, 0]

        for x in range(cols):
            row_color = [255 - c for c in row_color]
            color = [c for c in row_color]

            for y in range(rows):
                color = [255 - c for c in color]
                self.draw_square((x * blockSize, y * blockSize), blockSize,
                                 color=color)

    def checkerboard_fancy(self, blockSize=1):
        if self.width % blockSize != 0 \
                or self.height % blockSize != 0:
            raise ValueError('Block size will not fit image')
        cols = self.width // blockSize
        rows = self.height // blockSize
        row_color = True

        for x in range(cols):
            row_color = not row_color
            colorA = row_color
            green = int(round(x * 255 / (cols-1)))
            for y in range(rows):
                colorA = not colorA
                red = 255 - int(round(y * 255 / (rows-1)))
                blue = int(round(y * 255 / (rows-1)))

                if colorA:
                    color = [red, 255-green, 0]
                else:
                    color = [0, green, blue]
                self.draw_square((x * blockSize, y * blockSize), blockSize,
                                 color=color)

    def draw_square(self, origin, size, color=(0, 0, 0)):
        if size < 1:
            size = 1
        X, Y = origin

        for x in range(X, X + size):
            for y in range(Y, Y + size):
                self.pixel((x, y), color)

    def draw_hexagon_board(self):
        big_size = 120

        width = 10
        "Big main"
        self.draw_hexagon(*self.center, big_size, color=(255, 160, 0), width=width)
        "Surroundings"
        self.draw_smaller_hexes(self.center, 60, 300, big_size, width)
        self.draw_smaller_hexes(self.center, 60, 180, big_size, width)
        self.draw_smaller_hexes(self.center, 120, 240, big_size, width)
        self.draw_smaller_hexes(self.center, 240, 120, big_size, width)
        self.draw_smaller_hexes(self.center, 300, 180, big_size, width)
        self.draw_smaller_hexes(self.center, 300, 60, big_size, width)


    def draw_smaller_hexes(self, origin, angle, direction, big_size, width):
        small_size = big_size//3
        point = self.relative_point(*origin, angle, distance=big_size+small_size+width)
        point = self.relative_point(*point, direction, distance=small_size+width//2)
        print(-angle)        
        self.draw_hexagon(*point, small_size, color=(255, 60, 150), width=width//2)
        point = self.relative_point(*point, direction, distance=small_size*2)
        self.draw_hexagon(*point, small_size, color=(255, 60, 150), width=width//2)

        # mini = self.relative_point(*self.center, -60, distance=big_size-small_size)
        # self.draw_hexagon(*mini, 40, color=(255, 60, 150), width=5)

        # point = self.relative_point(*mini, 60, distance=small_size*2)
        # self.draw_hexagon(*point, 40, color=(255, 60, 150), width=5)

    def draw_hexagon(self, x0, y0, radius, color=(0, 0, 0), width=5):

        first = self.relative_point(x0, y0, 60, distance=radius)
        end_point = self.draw_line_angle(
            *first, 300, radius, color=color, width=width)
        end_point = self.draw_line_angle(
            *end_point, 240, radius, color=color, width=width)
        end_point = self.draw_line_angle(
            *end_point, 180, radius, color=color, width=width)
        end_point = self.draw_line_angle(
            *end_point, 120, radius, color=color, width=width)
        end_point = self.draw_line_angle(
            *end_point, 60, radius, color=color, width=width)
        end_point = self.draw_line_angle(
            *end_point, 0, radius, color=color, width=width)

    def draw_line(self, x0, y0, x1, y1, color=(0, 250, 0), width=3):
        self.draw.line((x0, y0, x1, y1), width=width, fill=color)

    def draw_line_angle(self, x0, y0, angle, distance,
                        color=(0, 0, 0), width=3):
        """
        Compass
               90
               |
         180- -+- - 0
               |
              270
        """

        x1, y1 = self.relative_point(x0, y0, angle, distance)
        self.draw.line((x0, y0, x1, y1), width=width, fill=color)
        return (x1, y1)

    def relative_point(self, x0, y0, angle, distance):
        angle = (angle % 360) * np.pi / 180
        x1 = x0 + np.cos(angle) * distance
        y1 = y0 - np.sin(angle) * distance
        return x1, y1

    def save(self, name=None):
        if not name:
            name = self.name
        self.picture.save(name + '.png')

    def pixel(self, pos, color=(0, 0, 0)):
        color = tuple(color)
        self.picture.putpixel(pos, color)


if __name__ == "__main__":
    width, height = 900, 900
    App = DrawMaster(size=(width, height), background=(80, 120, 150))
    App.draw_hexagon_board()
    App.save()

    print('\nEnd!!!'*5)
