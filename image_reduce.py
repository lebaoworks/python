from lib.os import morph_dir
import io, os
from PIL import Image

def reduce_image(image_path, heigh=1280):
    size = os.path.getsize(image_path)
    image = Image.open(image_path)
    if image.size[1] > heigh:
        ratio = heigh / image.size[1]
        image = image.resize((int(image.size[0]*ratio), int(image.size[1]*ratio)))
    image = image.convert('RGB')
    buffer = io.BytesIO()
    image.save(buffer, 'jpeg')#, quality=100, sampling=0)
    buffer.seek(0)
    buffer = buffer.read()
    if len(buffer) < size:
        return buffer
    return open(image_path, "rb").read()

def check(source_path):
    try:
        Image.open(source_path)
        return True
    except:
        return False

def do_reduce(source_path, destination_path):
    size = os.path.getsize(source_path)
    reduced = reduce_image(source_path)
    ratio = round( (size-len(reduced)) / size * 100, 2)
    s = os.path.basename(os.path.dirname(source_path))+"/"+os.path.basename(source_path)
    print(f"[+] {s} -> {ratio}%")
    open(os.path.splitext(destination_path)[0]+".jpg", "wb").write(reduced)

input_dir = r""
output_dir = r""
morph_dir(input_dir, output_dir, check, do_reduce)
