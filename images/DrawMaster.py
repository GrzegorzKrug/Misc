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

    def draw_hex_grid(self, tile_size=50, color=(0, 0, 0), width=10):
        cx, cy = self.center

        for direction in [1,2,3,4,5,6]:
            self.draw_recurent_hexes(cx, cy, tile_size, color, width,
                                     cur_dir=direction, cur_depth=0, max_depth=5)
        self.draw_hexagon(cx, cy, tile_size, color=(
            255, 255, 255), width=width)

    def draw_recurent_hexes(self, cx, cy, tile_size, color, width,
                            cur_dir, cur_depth, max_depth=10):
        point = self.get_hexagon_offset(cx, cy, tile_size, cur_dir)
        color = (25 * cur_dir, cur_dir % 3 * 25, cur_dir % 4 * 60)
        self.draw_hexagon(*point, tile_size, color=color, width=width)
        if cur_depth + 1 < max_depth:
            if cur_dir == 1:
                pass
                self.draw_recurent_hexes(*point, tile_size, color, width, 1, cur_depth+1, max_depth)
                self.draw_recurent_hexes(*point, tile_size, color, width, 2, cur_depth+1, max_depth)
                # self.draw_recurent_hexes(*point, tile_size, color, width, 6, cur_depth+1, max_depth)
            elif cur_dir == 2:
                self.draw_recurent_hexes(*point, tile_size, color, width, 2, cur_depth+1, max_depth)
            elif cur_dir == 3:
                self.draw_recurent_hexes(*point, tile_size, color, width, 2, cur_depth+1, max_depth)
                self.draw_recurent_hexes(*point, tile_size, color, width, 3, cur_depth+1, max_depth)
                # self.draw_recurent_hexes(*point, tile_size, color, width, 4, cur_depth+1, max_depth)
            elif cur_dir == 4:
                self.draw_recurent_hexes(*point, tile_size, color, width, 4, cur_depth+1, max_depth)
                self.draw_recurent_hexes(*point, tile_size, color, width, 5, cur_depth+1, max_depth)
            elif cur_dir == 5:
                self.draw_recurent_hexes(*point, tile_size, color, width, 5, cur_depth+1, max_depth)
            elif cur_dir == 6:
                self.draw_recurent_hexes(*point, tile_size, color, width, 5, cur_depth+1, max_depth)
                self.draw_recurent_hexes(*point, tile_size, color, width, 6, cur_depth+1, max_depth)
            else:
                pass

        # p1 = self.get_hexagon_offset(cx, cy, tile_size, 2)
        # self.draw_hexagon(*p1, tile_size, color=color, width=width)
        # p1 = self.get_hexagon_offset(cx, cy, tile_size, 3)
        # self.draw_hexagon(*p1, tile_size, color=color, width=width)
        # p1 = self.get_hexagon_offset(cx, cy, tile_size, 4)
        # self.draw_hexagon(*p1, tile_size, color=color, width=width)
        # p1 = self.get_hexagon_offset(cx, cy, tile_size, 5)
        # self.draw_hexagon(*p1, tile_size, color=color, width=width)
        # p1 = self.get_hexagon_offset(cx, cy, tile_size, 6)
        # self.draw_hexagon(*p1, tile_size, color=color, width=width)

    def draw_flower(self, origin, big_size=300, width=10):
        self.draw_hexagon(*origin, big_size,
                          color=(255, 160, 0), width=width)
        "Surroundings"
        self.draw_smaller_hexes(origin, 1, big_size, width)
        self.draw_smaller_hexes(origin, 2, big_size, width)
        self.draw_smaller_hexes(origin, 3, big_size, width)
        self.draw_smaller_hexes(origin, 4, big_size, width)
        self.draw_smaller_hexes(origin, 5, big_size, width)
        self.draw_smaller_hexes(origin, 6, big_size, width)

    def draw_smaller_hexes(self, origin, edge, big_size, width):
        small_size = big_size//3
        Edges = {1: (60, 300), 2: (60, 180), 3: (120, 240),
                 4: (240, 120), 5: (300, 180), 6: (300, 60)}
        angle, direction = Edges[edge]

        point = self.relative_point(*origin, angle,
                                    distance=big_size+small_size+width)
        point = self.relative_point(*point, direction,
                                    distance=small_size+width//2
                                    )
        point2 = self.relative_point(*point, direction, distance=small_size*2)

        self.draw_hexagon(*point, small_size,
                          color=(255, 60, 150), width=width//2)
        self.draw_hexagon(*point2, small_size,
                          color=(255, 60, 150), width=width//2)

    @staticmethod
    def get_hexagon_offset(x0, y0, radius, edge):
        xoffset = radius*3//2
        yoffset = np.sqrt(3)*radius//2
        if edge == 1:
            x1 = x0 + xoffset
            y1 = y0 - yoffset
        elif edge == 2:
            x1 = x0
            y1 = y0 - yoffset*2
        elif edge == 3:
            x1 = x0 - xoffset
            y1 = y0 - yoffset
        elif edge == 4:
            x1 = x0 - xoffset
            y1 = y0 + yoffset
        elif edge == 5:
            x1 = x0
            y1 = y0 + yoffset*2
        elif edge == 6:
            x1 = x0 + xoffset
            y1 = y0 + yoffset
        return x1, y1

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
    App.draw_hex_grid()
    App.save()

    print('\nEnd!!!'*5)
