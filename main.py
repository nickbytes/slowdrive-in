import os, time, sys, random

from PIL import Image
import ffmpeg


def generate_frame(in_filename, out_filename, time, width, height):
    (
        ffmpeg.input(in_filename, ss=time)
        .filter("scale", width, -1)
        .filter("pad", width, height, -1, -1)
        .output(out_filename, vframes=1)
        .overwrite_output()
        .run(capture_stdout=True, capture_stderr=True)
    )


# Ensure this is the correct path to your video folder
viddir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Videos/")

while 1:

    # Pick a random .mp4 video in your video directory
    currentVideo = ""
    while not (currentVideo.endswith('.mp4')):
        videoCount = len(os.listdir(viddir))
        randomVideo = random.randint(0, videoCount-1)
        currentVideo = os.listdir(viddir)[randomVideo]
    inputVid = viddir + currentVideo
    print(inputVid)
