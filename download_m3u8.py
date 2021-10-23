cache_path = "cache"

import datetime
import os
import threading
import requests
from queue import Queue

def job(queue):
     while True:
          try:
               path, url = queue.get_nowait()
          except:
               print("[*] Join")
               return
          for i in range(0, 5):
               try:
                    r = requests.get(url, headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}, stream=True, timeout=10)
                    with open(path, 'wb') as fp:
                         for chunk in r.iter_content(512000):
                              fp.write(chunk)
                              #print(f"{url} -> {len(chunk)}")
                    break
               except:
                    print(f"[!] Timeout: {url}")
          print(f"[+] {url}")
 
if __name__ == '__main__':
     import argparse
     parser = argparse.ArgumentParser(description='L0oA TOol')
     parser.add_argument('-i', type=str, required=True)
     parser.add_argument("-o", type=str, required=True)
     parser.add_argument("-t", type=int, default=64)
     args = parser.parse_known_args()[0]

     m3u8 = open(args.i,"rb").read().decode()     
     #Initalize cache
     try:
        os.makedirs(cache_path)
     except FileExistsError:
          if not os.path.isdir(cache_path):
               raise OSError("Path exists as file")
     chunk_infos = []
     for line in m3u8.split('\n'):
          if 'http' in line:
               print(f"[+] Chunk: {line}")
               chunk_infos.append(line)
     list_path = os.path.join(cache_path, "list.txt")
     with open(list_path, "w") as f:
          for i, path in enumerate(chunk_infos):
               f.write(f"file {i}\n")

     #Download
     queue = Queue()
     for i, url in enumerate(chunk_infos):
          queue.put((os.path.join(cache_path, str(i)), url))

     start = datetime.datetime.now().replace(microsecond=0)
     threads = []
     for i in range(args.t):
          thread = threading.Thread(target=job, args=(queue,))
          thread.start()
          threads.append(thread)
     for thread in threads:
          thread.join()
     end = datetime.datetime.now().replace(microsecond=0)
     print('Time to download:' + str(end-start))

     # os.system(f'ffmpeg -i {list_path} -vcodec copy -acodec copy -f mp4 {args.o}')
     os.system(f'ffmpeg -f concat -safe 0 -i {list_path} -c copy {args.o}')
     print('Video merge completed')

     over = datetime.datetime.now().replace(microsecond=0)
     print('Merge time:' + str(over-end))