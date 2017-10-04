# -*- coding: utf-8 -*-

import caffe
import numpy as np


#path to test image
filename = 'fish-bike.jpg'

#path to deploy prototxt and model file
file_deploy='deploy.prototxt'
file_model='bvlc_googlenet.caffemodel'

#load image
im = caffe.io.load_image(filename)

caffe.set_mode_cpu()

#load the model
net = caffe.Net(file_deploy,file_model,caffe.TEST);

#configure preprocessing
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
mean_file = np.array([104,117,123])
transformer.set_mean('data', mean_file)
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)
net.blobs['data'].reshape(1,3,224,224)


net.blobs['data'].data[...] = transformer.preprocess('data', im)

# run network
out = net.forward()

#extracting features from the layer 'pool5/7x7_s1'
good_features = net.blobs['pool5/7x7_s1'].data[...]

#predicted class
print out['prob'].argmax()



