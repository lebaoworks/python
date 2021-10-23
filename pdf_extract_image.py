import os, sys, io

# pip install PyMuPDF 
import fitz
from PIL import Image

from lib.os import assure_path
from lib.image import convert

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} path_to_pdf")
        exit(1)

    path = os.path.abspath(sys.argv[1]) + "_extracted"
    assure_path(path)

    doc = fitz.open(sys.argv[1])
    for page_index, page in enumerate(doc):
        for image_index, image in enumerate(page.getImageList()):
            # PDF use mask image as alpha layer of png
            xref = image[0]
            mask = image[1]
            print(f"[+] {page_index}_{image_index}",end='')
    
            base_image = Image.open(io.BytesIO(doc.extractImage(xref)['image']))
            if mask != 0:
                print(" -> add mask", end='')
                base_image = convert(base_image, "png")
                mask = Image.open(io.BytesIO(doc.extractImage(mask)["image"]))
                base_image.putalpha(mask)
            base_image.save(f"{path}/{str(page_index).zfill(3)}_{str(image_index).zfill(3)}.{base_image.format.lower()}", quality=100, sampling=0)
            
            print("")

            

