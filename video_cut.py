import sys
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: %s <file_name> <output_name> <start_time (s)> <end_time (s)> "%sys.argv[0])
        exit(1)
    ffmpeg_extract_subclip(sys.argv[1], float(sys.argv[3]), float(sys.argv[4]), sys.argv[2])