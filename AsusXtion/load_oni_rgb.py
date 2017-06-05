# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------

from primesense import openni2
import cv2
import sys
from functions.interface import get_video

if __name__ == '__main__':

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("/home/simone/libs/OpenNI2/Bin/x64-Release/")

    if len(sys.argv) > 1:
        file = sys.argv[1]
    else:
        print "***ERROR. Usage: python load_oni_rgb $PATH_TO_ONI_FILE"
        exit()

    dev = openni2.Device.open_file(file)
    print "RGB init"
    color_stream = dev.create_color_stream()
    color_stream.start()

    count = dev.playback.get_number_of_frames(color_stream)
    done = False
    while count is not 0:
        frame = get_video(color_stream)
        cv2.imshow('RGB', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            done = True
        count -= 1
    cv2.destroyAllWindows()
    color_stream.stop()
    openni2.unload()


# Do stuff here
