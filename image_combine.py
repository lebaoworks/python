from lib.image import combine
from PIL import Image
import sys

if __name__=='__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <image_1> <image_2> ... <image_n>")
        exit()
    images = [Image.open(sys.argv[i]) for i in range(1, len(sys.argv))]
    combined = combine([images])
    combined.save(f"combined.{images[0].format}", quality=100, sampling=0)
    