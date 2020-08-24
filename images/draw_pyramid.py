import os
from PIL import Image
import math
import time

time0 = time.time()

pic = Image.new('RGB',(250,250), (255,255,255))
width, height = pic.size
center = [int(width/2), int(height/2)]
x = 0
y = 0

pic.putpixel((center[0] + x, center[1] + y), (0,0,0))
size = 251    
for step in range(0,size):
    red = 255
    green = 255  
    blue = 255
    color = (0,0,0)    
    saturation = step/(size-105)
    for i in range(0,step):
        
        direction = step%4
        if direction == 0:  # go right
            x += 1
            color = (red,0,0)
        elif direction == 1:  # go bottom
            y -= 1
            color = (0, green, 0)
        elif direction == 2:  #go left
            x -= 1
            color = (0, 0, blue)
        else:  # got top
            y += 1
            color = (255,255,0)

        color = tuple(int(c*saturation) for c in color)
        try:
            pic.putpixel((center[0] + x, center[1] + y), color)
        except IndexError:
            break


pic.save('pyramid.png')


print('\nEnd!!!'* 3)
