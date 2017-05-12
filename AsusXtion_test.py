# --------------------------------------------------------
# OpenNI2 + OpenCV 2.4.13 + Asus Xtion
# Written by Simone Grazioso
# --------------------------------------------------------


from primesense import openni2
from primesense import _openni2 as c_api
import cv2
import numpy as np

#function to get RGB image from ASUS Xtion
def get_video():
	frame = color_stream.read_frame()
	frame_data = frame.get_buffer_as_uint8()
	img = print_rgb_frame(frame_data, np.uint8)
	return img
    
#function to get depth image from ASUS Xtion
def get_depth():
	frame = depth_stream.read_frame()
	frame_data = frame.get_buffer_as_uint16()
	dpt = print_depth_frame(frame_data, np.uint16)
	return dpt


def print_depth_frame(frame_data, thisType):
    img = np.frombuffer(frame_data, dtype=thisType)
    whatisit = img.size

    if whatisit == (640*480*1):
        img.shape = (1, 480, 640)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640*480*3):
        img.shape = (480, 640, 3)
    else:
        print "Frames are of size: ",img.size

    return img
    
def print_rgb_frame(frame_data, thisType):
    img = np.frombuffer(frame_data, dtype=thisType)

    whatisit = img.size

    if whatisit == (640*480*1):
        img.shape = (1, 480, 640)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640*480*3):
        img.shape = (480, 640, 3)
    else:
        print "Frames are of size: ",img.size

    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
    return img

if __name__ == '__main__':
	
	# path to OpenNI2/Bin/x64-Release/
	openni2.initialize("PATH_TO_OPENNI2")

	dev = openni2.Device.open_any()
	
	print "RGB init"
	color_stream = dev.create_color_stream()
	color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))
	color_stream.start()

	print "Depth init"
	depth_stream = dev.create_depth_stream()
	depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_100_UM, resolutionX = 640, resolutionY = 480, fps = 30))
	depth_stream.start()
	
	done = False
	while not done:
		k = cv2.waitKey(5)
		if k == 27:
			print "\tESC key detected!"
			done = True
			
		# retrieve rgb frame and depth
		frame = get_video()
		depth = get_depth()
		
		# apply colormap to depth
		depth = cv2.applyColorMap(depth.astype(np.uint8), cv2.COLORMAP_BONE)
		
		vis = np.concatenate((frame, depth), axis=1) #concatenate rgb and depth along y axis
		cv2.imshow('RGB + Depth',vis) #visualize both rgb and depth

	cv2.destroyAllWindows()
	color_stream.stop()
	depth_stream.stop()
	openni2.unload()
