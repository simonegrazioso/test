# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------

from __future__ import print_function
from primesense import openni2
from primesense import _openni2 as c_api
import cv2
import numpy as np
import sys
import time
from functions.interface import get_video, get_depth

if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == "RGBD":
            recording_mode_rgbd = True
            string_file = "RGBD"
        elif sys.argv[1] == "RGB":
            recording_mode_rgbd = False
            string_file = "RGB"
        else:
            print("Usage: python record_video RGB|RGBD (default is RGBD)")
            exit()
    else:
        recording_mode_rgbd = True
        string_file = "RGBD"  # default si RGBD

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("/usr/lib")

    dev = openni2.Device.open_any()

    print("RGB init")
    color_stream = dev.create_color_stream()
    color_stream.set_video_mode(c_api.OniVideoMode(
        pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
        resolutionX=640, resolutionY=480, fps=30))
    color_stream.start()

    if recording_mode_rgbd is True:
        print("Depth init")
        depth_stream = dev.create_depth_stream()
        depth_stream.set_video_mode(
            c_api.OniVideoMode(
                pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM,
                resolutionX=640, resolutionY=480, fps=30
            )
        )
        depth_stream.start()

    print("**** Press R to start Recording ****\n"
          "***** Press S for a Screenshot *****\n"
          "********** Press Q to Quit *********\n")
    done = False
    recording = False
    while not done:
        frame = get_video(color_stream)
        if recording_mode_rgbd is True:
            depth = get_depth(depth_stream)
            # apply colormap to depth
            depth = cv2.applyColorMap(depth.astype(np.uint8),
                                      cv2.COLORMAP_BONE)
            # concatenate rgb and depth along y axis
            vis = np.concatenate((frame, depth), axis=1)
        else:
            vis = frame

        cv2.imshow('{} Data'.format(string_file), vis)

        keypress = cv2.waitKey(1)
        if keypress & 0xFF == ord('r'):
            if recording is not True:
                recording = True
                filename = time.strftime(
                    "%Y.%m.%d-%H.%M.%S_{}_Data".format(string_file))
                rec = openni2.Recorder("oni/{}.oni".format(filename))
                rec.attach(color_stream, allow_lossy_compression=True)
                if recording_mode_rgbd is True:
                    rec.attach(depth_stream, allow_lossy_compression=True)
                rec.start()
                print("Recording... Press R again to stop")
            else:
                recording = False
                rec.stop()
                print("*** Saved {}.oni ***".format(filename))
        elif keypress & 0xFF == ord('s'):
            screen = time.strftime(
                "%Y.%m.%d-%H.%M.%S_{}_Data".format(string_file))
            cv2.imwrite("images/{}.png".format(screen), frame)
            print("Screen saved at images/{}.png".format(screen))
        elif keypress & 0xFF == ord('q'):
            done = True
            print("Quit.")
            break

    cv2.destroyAllWindows()
    color_stream.stop()
    depth_stream.stop()
    openni2.unload()


# Do stuff here
