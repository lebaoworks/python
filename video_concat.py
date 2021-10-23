from moviepy.editor import *
import os

videos = [file_name for file_name in os.listdir(".") if file_name.endswith(".asf")]
videos = [VideoFileClip(file_name) for file_name in videos]
final = concatenate_videoclips(videos)
final.write_videofile("concat.mp4")
