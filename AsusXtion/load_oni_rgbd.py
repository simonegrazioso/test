# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------

from primesense import openni2
import cv2
import numpy as np
import sys
from functions.interface import get_video, get_depth


if __name__ == '__main__':

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("/home/simone/libs/OpenNI2/Bin/x64-Release/")

    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        print "***ERROR. Usage: python load_oni_rgbd $PATH_TO_ONI_FILE"
        exit()
    dev = openni2.Device.open_file(file)
    print "RGB init"
    color_stream = dev.create_color_stream()
    color_stream.start()

    print "Depth init"
    depth_stream = dev.create_depth_stream()
    depth_stream.start()

    done = False
    while not done:
        frame = get_video(color_stream)
        depth = get_depth(depth_stream)
        # apply colormap to depth
        depth = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_BONE)

        # concatenate rgb and depth along y axis
        vis = np.concatenate((frame, depth), axis=1)
        cv2.imshow('RGB + Depth', vis)  # visualize both rgb and depth
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()
    color_stream.stop()
    depth_stream.stop()
    openni2.unload()


# Do stuff here
