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
import socket
from functions.interface import get_video, get_depth

TCP_IP = '0.0.0.0'
TCP_PORT = 50007

if __name__ == '__main__':

    string_file = "RGBD"  # default si RGBD

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("/usr/lib")
    
    print ("socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("bind")
    s.bind((TCP_IP, TCP_PORT))
    print ("listen")
    s.listen(True)
    print ("accept")
    conn, addr = s.accept()
    print ("Device open")
    dev = openni2.Device.open_any()


    print("**** Press R to start Recording ****\n"
          "***** Press S for a Screenshot *****\n"
          "********** Press Q to Quit *********\n")
    done = False
    recording = False
    while not done:
        try:
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

		length = recvall(conn, 16)
                stringData = recvall(conn, int(length))

                data = np.fromstring(stringData, dtype=np.uint8)
                #data = np.fromstring(stringData)
                frame = cv2.imdecode(data, 1)

                length_depth = recvall(conn, 16)
                stringData_depth = recvall(conn, int(length_depth))
                #stringData_depth = recvall(conn, int(length_depth))

                data_depth = np.fromstring(stringData_depth, dtype=np.uint16)
                #data = np.fromstring(stringData)
                depth = cv2.imdecode(data_depth, -1 )
                #cv2.imwrite("frames/depth_" + str(count) + ".png", depth)

                depth = cv2.applyColorMap(
                    depth.astype(np.uint8), cv2.COLORMAP_BONE)

                vis = np.concatenate(
                    (frame, depth.astype(np.uint8)), axis=1)
                cv2.imshow('RGB + Depth', vis)
                cv2.waitKey(1)
                #cv2.imwrite("frames/frame_" + str(count) + ".jpg", frame)

        except Exception as e:
		print(e)
                continue

	break

        cv2.destroyAllWindows()
        s.close()
        openni2.unload()



