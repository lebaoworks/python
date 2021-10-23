from PIL import Image, ImageCms
import sys

if __name__=='__main__':
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <image_in> <image_out>")
        exit()
    img = Image.open(sys.argv[1])
    img = ImageCms.profileToProfile(img, './color_profiles/SWOP2006_Coated3v2.icc', './color_profiles/sRGB2014.icc', renderingIntent=0, outputMode='RGB')
    img.save(sys.argv[3], quality=100, sampling=0)
    