from PIL import Image
from math import sqrt
import os
from fire import Fire


def rgb_average(image):
    return image.resize((1,1)).getpixel((0,0))

def rgb_distance(c1, c2):
    (r1,g1,b1) = c1
    (r2,g2,b2) = c2
    return sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

def get_images(path, frame_width, frame_height):
    files = os.listdir(path)
    images = []
    for file in files:
        filepath = os.path.abspath(os.path.join(path, file))
        images.append(Image.open(filepath).convert('RGB').resize((frame_width, frame_height)))
    return images

def convert_to_mosaic(filename, tilepath, width=100, height=100, save='NO', savepath='photomosaic.jpg'):
    image = Image.open(filename)

    image_width, image_height = image.size[0], image.size[1]
    frame_width, frame_height = int(image_width/width), int(image_height/height)
    
    frames = [[image.crop((x*frame_width, y*frame_height, frame_width*(x+1), frame_height*(y+1))) for y in range(height)] for x in range(width)]
    
    images = get_images(tilepath, frame_width, frame_height)
    
    new_grid = []
    for row in frames:
        new_row = []
        for frame in row:
            distances = [rgb_distance(rgb_average(frame), rgb_average(image)) for image in images]
            new_row.append(images[distances.index(min(distances))])
        new_grid.append(new_row)
    
    mosaic_image = Image.new('RGB', size=(frame_width*width, frame_height*height))
    for x,row in enumerate(new_grid):
        for y,frame in enumerate(row):
            mosaic_image.paste(frame, (x*frame_width, y*frame_height))
    mosaic_image.show()

    if save.upper() in ('Y','YES'):
        mosaic_image.save(savepath)


if __name__=='__main__':
    Fire(convert_to_mosaic)
