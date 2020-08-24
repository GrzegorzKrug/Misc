from PIL import Image

def get_rgb_array(input_image):
    width, height = input_image.size
    image = []  # empty output list
    
    for h in range(height):
        image.append([])  # new row
        for w in range(width):
            image[-1].append( list( input_image.getpixel((w,h)) ) )
    return image
    
def update_image_from_array_image(input_image, image_ref):
    height, width = [len(input_image),len(input_image[0])]
    print((width, height))
    print(image_ref.size)
    if (width, height) != image_ref.size:
        raise ValueError

    for h in range(height):
        for w in range(width):
            pixels = input_image[h][w]
            image_ref.putpixel((w,h), tuple(pixels))

def filter_black_white(array):
    new_array = array.deepcopy()
    for r,row in enumerate(array):
        for e,element in enumerate(row):
            light = sum(element)
            
            
bunny = Image.open('bunnies.jpg')

bunny_crop = bunny.crop((120,100, 750, 550))
bunny_crop.save('bunnies_cropped.jpg')

width, height = bunny_crop.size
bunny_crop = bunny_crop.resize((int(width/5), int(height/5)))
width, height = bunny_crop.size

color_array = get_rgb_array(bunny)
for r,row in enumerate(color_array):
    for e,element in enumerate(row):
        element[0], element[1] = element[1], element[0]
update_image_from_array_image(color_array, bunny)

##for x in range(8):
##    bunny_crop = bunny_crop.transpose(Image.FLIP_LEFT_RIGHT)
##    bunny.paste(bunny_crop, ((width+2)*x, 0))
##    
##for x in range(8):
##    bunny.paste(bunny_crop, (0, (2+height)*x))





bunny.save('bunny_remastered.png')
