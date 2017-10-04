import os
import sys
import timeit

import numpy
import cv2
import caffe

folder="training/"
N=1
listing = os.listdir(folder)
mean = numpy.zeros((1,3,28,28,))
for file in listing:
     # rgb mean
    img = cv2.imread(folder+file)
    img2 = numpy.asarray(img)
    img2=img2.astype(float)
    mean[0][0] += img2[:, :, 0]
    mean[0][1] += img2[:, :, 1]
    mean[0][2] += img2[:, :, 2]
    N+=1
mean[0] /= N

mean=mean.astype(int)
blob = caffe.io.array_to_blobproto(mean)
with open('mean_image3.binaryproto', 'wb' ) as f :
    f.write( blob.SerializeToString())