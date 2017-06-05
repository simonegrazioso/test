# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------

from primesense import openni2
import cv2
import numpy as np
import sys
from functions.interface import get_video, get_depth


ALCOR = False  # if we use ALCOR Asus Xtion, False otherwise


# function to get RGB image from ASUS Xtion

if __name__ == '__main__':

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("/home/simone/libs/OpenNI2/Bin/x64-Release/")

    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        print "***ERROR. Usage: python convert_rgbd_to_rgb $PATH_TO_ONI_FILE"
        exit()

    dev = openni2.Device.open_file(file)
    print "RGB init"
    color_stream = dev.create_color_stream()
    color_stream.start()

    print "Depth init"
    depth_stream = dev.create_depth_stream()
    depth_stream.start()

    print("Start converting {} from RGBD to RGB.".format(file))
    rec = openni2.Recorder("{}_converted_to_rgb.oni".format(file[:-4]))
    rec.attach(color_stream, allow_lossy_compression=True)
    rec.start()
    done = False
    count = dev.playback.get_number_of_frames(color_stream)
    while count is not 6:
        print count
        frame = get_video(color_stream)
        depth = get_depth(depth_stream)
        # apply colormap to depth
        depth = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_BONE)

        # concatenate rgb and depth along y axis
        vis = np.concatenate((frame, depth), axis=1)
        cv2.imshow('RGB + Depth', vis)  # visualize both rgb and depth
        if cv2.waitKey(1) & 0xFF == ord('q'):
            rec.stop()
            break
        count -= 1
    print("Saved in {}_converted_to_rgb.oni".format(file[:-4]))
    cv2.destroyAllWindows()
    color_stream.stop()
    depth_stream.stop()
    openni2.unload()


# Do stuff here
