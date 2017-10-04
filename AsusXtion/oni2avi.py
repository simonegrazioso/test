# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------

from primesense import openni2
import cv2
import numpy as np
import sys
import os
from functions.interface import get_video, get_depth

FPS = 30
fourcc = cv2.VideoWriter_fourcc(*'XVID')

# can also accept the path of the OpenNI redistribution
openni2.initialize("/usr/lib")

if len(sys.argv) > 1:
	file = sys.argv[1]
	print file
else:
	print "***ERROR. Usage: python extract_frames_from_oni $PATH_TO_ONI_FILE"
        exit()
dev = openni2.Device.open_file(file)

print "RGB init"
color_stream = dev.create_color_stream()
color_stream.start()
print "Depth init"
depth_stream = dev.create_depth_stream()
depth_stream.start()

done = False
count = 0
i = dev.playback.get_number_of_frames(color_stream)
print i
directory = file.rstrip('.oni')
if not os.path.exists(directory):
	os.makedirs(directory)
    
frame = get_video(color_stream)
frame_height , frame_width, _ = frame.shape

	# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
	#fourcc = cv2.VideoWriter_fourcc(directory+'.avi',cv2.VideoWriter_fourcc('M','J','P','G'), FPS, (frame_width,frame_height))
out = cv2.VideoWriter(directory+'.avi',fourcc, FPS,(frame_width,frame_height))

while count < i:
	frame = get_video(color_stream)    
        out.write(frame)
        count += 1
	if (count%10)==0:
		print 'Frame ' + str(count) +' / ' + str(i) 
        if cv2.waitKey(1) & 0xFF == ord('q'):
		break



cv2.destroyAllWindows() 
color_stream.stop()
out.release()
openni2.unload()

