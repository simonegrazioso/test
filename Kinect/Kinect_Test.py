#import the necessary modules
import freenect
import cv2
import numpy as np
 
#function to get RGB image from kinect
def get_video():
    array,_ = freenect.sync_get_video()
    array = cv2.cvtColor(array,cv2.COLOR_RGB2BGR)
    return array
 
#function to get depth image from kinect
def get_depth():
    array,_ = freenect.sync_get_depth()
    array = array.astype(np.uint8)
    return array
 
if __name__ == "__main__":
	while 1:
		# quit program when 'esc' key is pressed
		k = cv2.waitKey(5) & 0xFF
		if k == 27:
			break
		#get a frame from RGB camera
		frame = get_video()
		#get a frame from depth sensor
		depth = get_depth()
		depth = cv2.cvtColor(depth,cv2.COLOR_GRAY2BGR)
		#display depth image
		vis = np.concatenate((frame, depth.astype(np.uint8)), axis=1) #concatenate rgb and depth
		cv2.imshow('RGB + Depth',vis) #visualize both rgb and depth
		
	cv2.destroyAllWindows()

