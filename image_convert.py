from lib.os import morph_dir
import io, os
from PIL import Image

def check(source_path):
    try:
        Image.open(source_path)
        return True
    except:
        return False

def do_convert(source_path, destination_path):
    s = os.path.splitext(destination_path)[0]+".png"
    Image.open(source_path).save(s, quality=100, sampling=0, format='png')
    print(f"[+] {s}")

if __name__ == "__main__":
    morph_dir(
        "/mnt/d/[Game]/_MA/[__Done/[Takahama Tarou]/Taimanin Asagi Chigyaku no Ankoku Yuugi [English]",
        "/mnt/d/[Game]/_MA/[__Done/[Takahama Tarou]/Taimanin Asagi Chigyaku no Ankoku Yuugi [English]/png", check, do_convert)
