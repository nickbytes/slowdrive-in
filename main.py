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


# Pick a random .mp4 video in your video directory
currentVideo = ""
while not (currentVideo.endswith(".mp4")):
    videoCount = len(os.listdir(viddir))
    randomVideo = random.randint(0, videoCount - 1)
    currentVideo = os.listdir(viddir)[randomVideo]
inputVid = viddir + currentVideo

# print input movie
print(inputVid)

# Ensure this matches your particular screen or desired dimensions
width = 800
height = 480

# Check how many frames are in the movie
frameCount = int(ffmpeg.probe(inputVid)["streams"][0]["nb_frames"])

# Pick a random frame
frame = random.randint(0, frameCount)

# Convert that frame to Timecode
msTimecode = "%dms" % (frame * 41.666666)

# Use ffmpeg to extract a frame from the movie, crop it, letterbox it and save it as grab.jpg
generate_frame(
    inputVid,
    f"Images/{frame}-{os.path.splitext(currentVideo)[0]}.jpg",
    msTimecode,
    width,
    height,
)

# Open grab.jpg in PIL
pil_im = Image.open(f"Images/{frame}-{os.path.splitext(currentVideo)[0]}.jpg")

# Dither the image into a 1 bit bitmap (Just zeros and ones)
pil_im = pil_im.convert(mode="1", dither=Image.FLOYDSTEINBERG)

print("Diplaying frame %d of %s" % (frame, currentVideo))

pil_im.save(fp=f"Images/{frame}-{os.path.splitext(currentVideo)[0]}.jpg")

# now you gotta do something with these images
