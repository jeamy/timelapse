import cv2
import numpy as np
import glob
import sys
from io import StringIO
import time
import datetime
import os
import pathlib

ROOT_PATH = "/media/image/webcams"
VIDEO_PATH = "/media/image/webcams/video"


class VideoMaker:
    def __init__(self, camera_name, video_name):
        self.camera_name = camera_name
        self.video_name = video_name
        self.stamptext = camera_name
        self.input_path = ""
        self.ouput_path = ""
        self.frameSize = (1080, 1080)
        self.subdir = "2021-02-26"

    def Update(self):

        self.input_path = os.path.join(
            ROOT_PATH, self.camera_name, self.subdir, "*.jpeg")
        self.ouput_path = os.path.join(
            VIDEO_PATH, self.video_name + "-" + self.subdir + ".avi")
        pathlib.Path(VIDEO_PATH).mkdir(parents=True, exist_ok=True)

        print("Writing video from {0} \nto {1} ...".format(
            self.input_path, self.ouput_path))

        files = glob.glob(self.input_path)
        files.sort(key=os.path.getmtime)
        # print("\n".join(files))

        for file in files:
            img = cv2.imread(file)
            height, width, layers = img.shape
            self.frameSize = (width, height)
            break

        print("Size {0} x {1} ...".format(width, height))
        out = cv2.VideoWriter(self.ouput_path,
                              cv2.VideoWriter_fourcc(*'DIVX'), 20,
                              self.frameSize)

        for file in files:
            print("Reading {0} ...".format(file))
            img = cv2.imread(file)
            out.write(img)

        out.release()
        print("Done!")


if __name__ == "__main__":
    cameras = []
    cameras.append(VideoMaker("D50", "D50"))
    cameras.append(VideoMaker("D51", "D51"))
    cameras.append(VideoMaker("D52", "D52"))
    cameras.append(VideoMaker("D53", "D53"))

    print("Making video from {0} cameras ...".format(len(cameras)))

    for camera in cameras:
        camera.Update()
