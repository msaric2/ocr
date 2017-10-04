import numpy as np
import matplotlib.pyplot as plt
import sys
import caffe
import caffe.proto.caffe_pb2 as caffe_pb2
import cv2


def ClassifyImage(input_image):
    # Set the right path to your model definition file, pretrained model weights,
    # and the image you would like to classify.
    MODEL_FILE = 'caffee/lenetdeployDigitsLetters.prototxt'
    PRETRAINED = 'caffee/trainedModelsLetters/_iter_3650_allV6.caffemodel'      #_iter_3650_allV6.caffemodel

    #im = caffe.io.load_image(filename)

    # load the model
    caffe.set_mode_cpu()
    #caffe.set_device(0)
    net = caffe.Net(MODEL_FILE, PRETRAINED,caffe.TEST)

    print "successfully loaded classifier"

    #convert binaryproto to npy
    blob = caffe.proto.caffe_pb2.BlobProto()

    data = open('mean_image7.binaryproto' , 'rb' ).read()
    blob.ParseFromString(data)
    arr = np.array(caffe.io.blobproto_to_array(blob))
    mean_file = arr[0]
    #np.save(sys.argv[2], out)
    #

    # data = np.array(blob.data)
    #mean_file = np.array( caffe.io.blobproto_to_array(blob) )
    #out = arr[0]


    #configure preprocessing
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    #mean_file = np.array([110,110,110])
    transformer.set_mean('data', mean_file)
    transformer.set_transpose('data', (2,0,1))
    transformer.set_channel_swap('data', (2,1,0))
    transformer.set_raw_scale('data', 255.0)
    net.blobs['data'].reshape(1,3,28,28)

    #preprocess image
    net.blobs['data'].reshape(1,        # batch size
                              3,         # 3-channel (BGR) images
                              28, 28)

    #input_image=input_image-(input_image-0.5)
    net.blobs['data'].data[...] = transformer.preprocess('data', input_image)
    #shift mean near 0
    net.blobs['data'].data[...]=net.blobs['data'].data[...]-net.blobs['data'].data[...].mean()

    output = net.forward()
    output_prob = output['prob'][0]
    labels = np.loadtxt('labelsDigitsLetters.txt', str, delimiter='\t')
    return labels[output_prob.argmax()]
   # print 'output label:', labels[output_prob.argmax()]



    #print 'predicted class is:', output_prob.argmax()



f = open("results.txt", 'w')
for i in range(1,23,1):
    labelWord=""
    for j in range(3):
        filename="singleChars/char"+str(i)+"_"+str(j)+".tif"

        # img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # cv2.equalizeHist(img,img)
        #cv2.imwrite(filename, img)
        input_image = caffe.io.load_image(filename)
        label=ClassifyImage(input_image)
        labelWord=labelWord+label
    f.write(labelWord+'\n')
