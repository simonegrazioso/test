import cv2
import numpy as np
from config import ALCOR

# function to get RGB image from ASUS Xtion


def get_video(color_stream):
    frame = color_stream.read_frame()
    frame_data = frame.get_buffer_as_uint8()
    img = print_rgb_frame(frame_data, np.uint8)
    if ALCOR is not True:
        img = cv2.flip(img, 1)
    return img


# function to get depth image from ASUS Xtion


def get_depth(depth_stream):
    frame = depth_stream.read_frame()
    frame_data = frame.get_buffer_as_uint16()
    dpt = print_depth_frame(frame_data, np.uint16)
    if ALCOR is not True:
        dpt = cv2.flip(dpt, 1)
    return dpt


def print_depth_frame(frame_data, thisType):
    img = np.frombuffer(frame_data, dtype=thisType)
    whatisit = img.size

    if whatisit == (640 * 480 * 1):
        img.shape = (1, 480, 640)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640 * 480 * 3):
        img.shape = (480, 640, 3)
    else:
        print "Frames are of size: ", img.size

    return img


def print_rgb_frame(frame_data, thisType):
    img = np.frombuffer(frame_data, dtype=thisType)

    whatisit = img.size

    if whatisit == (640 * 480 * 1):
        img.shape = (1, 480, 640)
        img = np.concatenate((img, img, img), axis=0)
        img = np.swapaxes(img, 0, 2)
        img = np.swapaxes(img, 0, 1)
    elif whatisit == (640 * 480 * 3):
        img.shape = (480, 640, 3)
    else:
        print "Frames are of size: ", img.size

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img
