import sys
import math
from PIL import Image

ASCII_CHARS = '@#()!<>+,. '

def scale_image(image, new_width):
    width, height = image.size
    #*1/2 to maintain image's ratio in text format
    ratio = height/width *1/2
    new_height = int(new_width*ratio)
    return image.resize((new_width,new_height))

def image_to_chars(image, chars):
    width, height = image.size

    #To Grayscale
    image = image.convert('L')

    #Pixels -> characters
    range_width = math.ceil(256/len(chars))
    pixels = list(image.getdata())
    mapped = [chars[pixel_value//range_width] for pixel_value in pixels]

    return "\n".join([''.join(mapped[index:index+width]) for index in range(0, len(mapped), width)])
  
if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <image> [<width>]!"%sys.argv[0])
        exit()
        
    image = Image.open(sys.argv[1])
    new_width, _ = image.size
    if len(sys.argv) == 3:
        new_width = int(sys.argv[2])
    image = scale_image(image,new_width)
    
    image_ascii = image_to_chars(image,ASCII_CHARS)
    print(image_ascii)
