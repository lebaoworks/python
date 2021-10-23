import cv2
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} file")
        exit(1)
    vidcap = cv2.VideoCapture(sys.argv[1])
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite("extracted/%4d.jpg"%count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1