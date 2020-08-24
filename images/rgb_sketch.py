import os
from PIL import Image
import math
import time

time0 = time.time()

pic = Image.new('RGB',(1000,1000), (255,255,255))
width, height = pic.size
middle = 700
for step in range(1000):
    for i in range(20000):
        if abs(middle - step) == 0:
            x = i
        else:
            x = int(0.12 * i * abs(middle - step))
        y = step # drawing each row
        
        red = int(x*255/width)
        green = int(255- math.sqrt((2*x*255/width)**2 + (2*y*255/height)**2))  # Green is in center and disapears in middle of drawing
        blue = int(y*255/height)
        color = (red,green,blue)
        
        try:
            pic.putpixel((x,y), color)
        except IndexError:
            break

pic.save('RGB.png')


print('\nEnd!!!'*5)
