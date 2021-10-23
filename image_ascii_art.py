import sys
from PIL import Image
from lib.image import ascii_art

ASCII_CHARS = '@#()!<>+,. '

def scale_image(image, new_width):
    width, height = image.size
    #*1/2 to maintain image's ratio in text format
    ratio = height/width * 1/2
    new_height = int(new_width*ratio)
    return image.resize((new_width,new_height))

if __name__=='__main__':
    if len(sys.argv) < 2:
        print("Usage: %s <image> [<width>]!"%sys.argv[0])
        exit()
        
    image = Image.open(sys.argv[1])
    new_width = int(sys.argv[2]) if len(sys.argv) == 3 else image.size[0]
    image = scale_image(image,new_width)
    image_ascii = ascii_art(image, ASCII_CHARS)
    print(image_ascii)
