import os
from PIL import Image, ImageChops

# Extract differences between base and masked
def make_mask(base, masked):
    img1 = base.convert("RGBA")
    img2 = masked.convert("RGBA")
    img1_data = img1.load()
    img2_data = img2.load()
    width, height = img2.size
    for y in range(height):
        for x in range(width):
            if img1_data[x, y] == img2_data[x, y]:
                img2_data[x, y] = (0, 0, 0, 0)
    return img2

# Apply mask over base
def apply_mask(base, mask):
    img1 = base.convert("RGBA")
    img2 = mask.convert("RGBA")
    img1_data = img1.load()
    img2_data = img2.load()
    width, height = img2.size
    for y in range(height):
        for x in range(width):
            if img2_data[x, y] != (0, 0, 0, 0):
                img1_data[x, y] = img2_data[x, y]
    img1 = img1.convert(base.mode)
    return img1

def do_make_mask(base_path, masked_path, mask_path):
    masked_files = os.listdir(masked_path)
    try:
        os.makedirs(mask_path)
    except:
        pass
    for file_name in masked_files:
        print(file_name)
        base_img   = Image.open(os.path.join(base_path, file_name))
        masked_img = Image.open(os.path.join(masked_path, file_name))
        mask = make_mask(base_img, masked_img)
        mask.save(os.path.join(mask_path, file_name), "PNG", quality=100, sampling=0)

def do_apply_mask(base_path, mask_path, output_path):
    mask_files = os.listdir(mask_path)
    try:
        os.makedirs(output_path)
    except:
        pass
    for file_name in mask_files:
        print(file_name)
        base_img = Image.open(os.path.join(base_path, file_name))
        mask_img = Image.open(os.path.join(mask_path, file_name))
        masked_img = apply_mask(base_img, mask_img)
        masked_img.save(os.path.join(output_path, file_name), quality=100, sampling=0)


base_path = r""
masked_path = r""
mask_path = r""
output_path = r""
do_make_mask(base_path, masked_path, mask_path)
do_apply_mask(base_path, mask_path, output_path)