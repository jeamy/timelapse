#!/usr/bin/python

import sys
from cv2 import cv2
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from urllib.request import urlopen
from io import StringIO
import time
import datetime
import os
import pathlib

ROOT_PATH = "/media/data/ZM-Bilder"

# Number of seconds between frames:
LAPSE_TIME = 600

# Name of truetype font file to use for timestamps (should be a monospace font!)
FONT_FILENAME = "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf"

# Format of timestamp on each frame
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

# Command to batch convert mjpeg to mp4 files:
#  for f in *.mjpeg; do echo $f ; avconv -r 30000/1001 -i "$f" "${f%mjpeg}mp4" 2>/dev/null ; done


class Camera:
    def __init__(self, name, url, filename):
        self.name = name
        self.url = url
        self.filename = filename
        self.video = cv2.VideoCapture(url)
        self.stamptext = name
        self.outputpath = os.path.join(ROOT_PATH, name)
        pathlib.Path(self.outputpath).mkdir(parents=True, exist_ok=True)

    def __del__(self):
        self.video.release()

    def CaptureImage(self):
        ret, frame = self.video.read()
        print("Got image from {0} camera".format(self.name))
        imageRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return Image.fromarray(imageRGB)

    def TimestampImage(self, image):
        draw_buffer = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_FILENAME, 32)
        timestamp = datetime.datetime.now()
        self.stamptext = "{0} - {1}".format(
            timestamp.strftime(TIMESTAMP_FORMAT), self.name)
        draw_buffer.text((5, 5), self.stamptext, font=font)

    def SaveImage(self, image):
        with open(os.path.join(self.outputpath, self.stamptext), "a+b") as video_file:
            image.save(video_file, "JPEG")
            video_file.flush()

    def Update(self):
        image = self.CaptureImage()
        # self.TimestampImage(image)
        self.SaveImage(image)
        print("Captured image from {0} camera to {1}".format(
            self.name, self.filename))


if __name__ == "__main__":
    cameras = []
    cameras.append(Camera(
        "D50", "rtsp://admin:123456@192.168.8.50:554/h264Preview_01_main", "D50.mjpeg"))
    cameras.append(
        Camera("D51", "rtsp://admin:12345@192.168.8.51:554/live/main", "D51.mjpeg"))
    cameras.append(Camera(
        "D52", "rtsp://admin:123456@192.168.8.52:554/h264Preview_01_main", "D52.mjpeg"))
    cameras.append(
        Camera("D53", "rtsp://prosmart:asgard69@192.168.8.53/stream=0", "D53.mjpeg"))

    print("Capturing images from {0} cameras every {1} seconds...".format(
        len(cameras), LAPSE_TIME))

    try:
        while (True):
            for camera in cameras:
                camera.Update()

            time.sleep(LAPSE_TIME)

    except KeyboardInterrupt:
        print("\nExit requested, terminating normally")
        sys.exit(0)
