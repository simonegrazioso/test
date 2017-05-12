# based on caffe: https://github.com/BVLC/caffe


#Let's import the necessary packages:
import sys
import cv2
import numpy as np
import caffe

#We will extract the feature vector from the following input image file:
input_image_file = sys.argv[1]

#This is the output text file where the line-separated feature vector will be stored:
output_file = sys.argv[2]

#We will be using a pretrained model file. You can download it from here (http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel):
model_file = 'bvlc_reference_caffenet.caffemodel'

#Specify the corresponding deploy prototxt file:
deploy_prototxt = 'models/bvlc_reference_caffenet/deploy.prototxt'

#We are now ready to initialize the convolutional neural network:
net = caffe.Net(deploy_prototxt, model_file, caffe.TEST)

#Let's say we want to extract the feature vector from the layer 'fc7' in the network. Define it:
layer = 'fc6'
if layer not in net.blobs:
    raise TypeError("Invalid layer name: " + layer)

#We need to specify the image mean file for the image transformer:
imagemean_file = 'python/caffe/imagenet/ilsvrc_2012_mean.npy'

#We need to define the transformer in order to preprocess the input image before feeding it into the network:
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', np.load(imagemean_file).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_raw_scale('data', 255.0)

#Reshape the network blob (if needed) to the shape needed for the current CNN architecture being used:
net.blobs['data'].reshape(1,3,227,227)

#Load the input image:
img = caffe.io.load_image(input_image_file)

#Run the image through the preprocessor:
net.blobs['data'].data[...] = transformer.preprocess('data', img)

#Run the image through the network:
output = net.forward()

print net.blobs[layer].data[0]
print net.blobs[layer].data[0].shape

#Extract the feature vector from the layer of interest:
with open(output_file, 'w') as f:
    np.savetxt(f, net.blobs[layer].data[0], fmt='%s', delimiter='\n')
    
#Go ahead and open the output text file. You will see a text containing 4096 lines,
#where each line contains a floating point value. This is the 4096-dimensional feature vector!
