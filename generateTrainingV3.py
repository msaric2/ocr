# -*- coding: utf-8 -*-
"""
Created on Fri Oct  7 22:24:09 2016

@author: Matko
"""

import os
import sys
import timeit

import numpy
import cv2
import caffe
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
from PIL import ImageOps

imagesIndex=range(1,100)
target=numpy.ndarray(10)
target==numpy.float64(target)
    #trainSet[0]=np.array()
   # imgTensor=numpy.empty()

def createSamples(filename,label,labelFont,folderTrain,folderTest):


    imgOriginal = cv2.imread(filename)
    imgOriginal=cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)

    imgOriginal = cv2.resize(imgOriginal, (28, 28), cv2.INTER_CUBIC)
    height, width=imgOriginal.shape[:2]
    mask=cv2.imread("lightningMask.tif")
    mask=cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    #mask=mask.convert('LA')
    mask=cv2.resize(mask,(28,28),cv2.INTER_CUBIC)
    counter=1
    counterTest=1

    flagTest = 0  # mark the test images
    for i1 in range(2):   # noise deviation
        for i2 in range(2):    #blur
            for i3 in range(4):  #blending alfa
                for i4 in range(2): # msk luminance level
                    for i6 in range(-4,4,2):  # rotation
                        img=imgOriginal
                        #adding noise
                        noise=numpy.zeros((28,28),numpy.uint8)
                        m = (120)
                        s = (5*(i1+1))
                        cv2.randn(noise, m, s)
                        img = cv2.addWeighted(img, 0.9, noise, 0.1, 0)
                        # img=imgOriginal+noise

                        #cv2.add(imgOriginal,noise,0,)
                        # if i1 == 2:
                        #     #img = cv2.GaussianBlur(img, (3, 3), 0)
                        #     retval, img = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
                        #     img=img*(i1*1.5)
                        if i2==0:
                            img=cv2.blur(img,(3,3))
                        step=0.1  #train=0.2 test=0.3
                        alfa = 1 - i3 * step;
                        mask2=mask-(i4+1)*10;
                        img = cv2.addWeighted(img, alfa, mask2, (1 - alfa), 0)
                        img=cv2.resize(img,(28,28),cv2.INTER_CUBIC)

                        cols,rows=img.shape
                        M=numpy.float32([[0,0,0], [0,0,0]])
                        M = cv2.getRotationMatrix2D((cols, rows), i6, 1)
                        img = cv2.warpAffine(img, M, (cols, rows))

                        r5 = 4  # train=0.2 test=0.3
                        for i5 in range(r5):  #add borders
                                step = 1
                                # imgBackground = numpy.zeros((height + 4, width + 4, 3), numpy.uint8)
                                # imgBackground =cv2.resize(mask, (32, 32), cv2.INTER_CUBIC);

                                imgBackground = cv2.resize(img, (32, 32), cv2.INTER_CUBIC);

                                # imgBackground[i5*step:(i5*step+28),i5*step:(i5*step+28)]=img
                                # imgBackground = cv2.copyMakeBorder(imgBackground, 4, 4, 4, 4, cv2.BORDER_REFLECT)
                                imgBackground = cv2.copyMakeBorder(img, i5*step, i5*step, i5*step, i5*step, cv2.BORDER_REFLECT)
                                imgBackground = cv2.resize(imgBackground, (28, 28), cv2.INTER_CUBIC)
                                # imgBackground=imgBackground-imgBackground.mean()
                                #calcualate eman
                                mean = cv2.mean(imgOriginal)

                                imgBackgroundRGB = numpy.zeros((28, 28, 3), numpy.uint8)
                                imgBackgroundRGB[:,:,0]=imgBackground
                                imgBackgroundRGB[:, :, 1] = imgBackground
                                imgBackgroundRGB[:, :, 2] = imgBackground
                                if counter % 10>0:
                                     if flagTest==1:
                                         counter=counter-1
                                         flagTest=0
                                     filename2 = folderTrain + label + "_" + labelFont+"_"+ str(counter) + '.jpg'
                                     cv2.imwrite(filename2, imgBackgroundRGB)
                                     counter = counter + 1
                                else:
                                    filename2 = folderTest + label + "_"+ labelFont+"_" + str(counterTest) + '.jpg'
                                    # imgBackgroundRGB=numpy.zeros((28,28,3),numpy.uint8)
                                    # imgBackgroundRGB[:,:,0]=imgBackground
                                    # imgBackgroundRGB[:, :, 1] = imgBackground;
                                    # imgBackgroundRGB[:, :, 2] = imgBackground;
                                    #
                                    #imgBackgroundRGB=cv2.cvtColor(imgBackground,  cv2.COLOR_GRAY2BGRA)

                                    cv2.imwrite(filename2, imgBackgroundRGB)
                                    counterTest = counterTest + 1
                                    counter = counter + 1
                                    flagTest = 1  #mark the jump in counter

                # img=img-img.mean();
                # cv2.imwrite(filename2,img)





def createFileList(folder,filename,NumOfExamples):
    #f = open('FileListTraining.txt', 'w')
    f = open(filename, 'w')
    for label in range(10):
        for counter in range(NumOfExamples):
            for font in range(1, 3):
                # line = folder + str(label) + "_" + str(counter+1) + '.jpg '+str(label)+'\n'
                line = folder + str(label) + "_"+str(font)+"_" + str(counter + 1) + '.jpg ' + str(label) + '\n'
                f.write(line)

def createFileListLetters(folder, filename, NumOfExamples):   # number of examples per character

    letters="ABCDEFGHIJP"
    f = open(filename, 'w')
    for label in range(11):
        for counter in range(NumOfExamples):
            letters = "ABCDEFGHIJP"
            for label in range(10, 21):
                for counter in range(NumOfExamples):
                    for font in range(1, 3):
                         line = folder + str(label) + "_" + str(counter + 1) + '.jpg ' + str(label) + '\n'
                         f.write(line)
                        #line = folder + str(label) + "_" + str(font) + "_" + str(counter + 1) + '.jpg ' + str(
                      #  for font in range(1, 3):
                # line = folder + str(label) + "_" + str(counter + 1) + '.jpg ' + str(label) + '\n'
                #line = folder + str(label) + "_" + str(font) + "_" + str(counter + 1) + '.jpg ' + str(label) + '\n'

                # counter=counter+1




def createFileListDigitsLetters(folder, filename, NumOfExamples):
    # f = open('FileListTraining.txt', 'w')
    f = open(filename, 'w')
    for label in range(21):
        for counter in range(NumOfExamples):
            for font in range(1, 4):
                # line = folder + str(label) + "_" + str(counter+1) + '.jpg '+str(label)+'\n'
                line = folder + str(label) + "_" + str(font) + "_" + str(counter + 1) + '.jpg ' + str(
                    label) + '\n'
                f.write(line)



# def createTestSet(folderTrain,folderTest,NumOfExamples):
#     for label in range(11):
#         step=NumOfExamples/10
#         for i in range(1,NumOfExamples,step):
#             fileName=folderTrain+"/"+str(label)+"_"+str(i)+".jpg"

# createFileListLetters("trainingLetters/", "FileListTrainingLetters.txt", 117)
# createFileListLetters("testLetters/", "FileListTestLetters.txt", 11)

# outputFolder = "trainingLetters/"
# letters="ABCDEFGHIJP"
# i=0
# for c in letters:
#     for f in range(1,3):
#         createSamples("trainingLetters/templates/letter" + c + "_"+str(f)+".tif", str(i),str(f), "trainingLetters/","testLetters/")
#     i = i + 1


# createSamples(filename,label,labelFont,folderTrain,folderTest):

createFileListDigitsLetters("training/","FileListTrainingDigitsLetters.txt",466)
createFileListDigitsLetters("test/","FileListTestDigitsLetters.txt",46)
outputFolder = "training/"
letters="ABCDEFGHIJP"
i=0
#creating training set for digits
for i in range(10):
    for f in range(1, 4):
        createSamples("trainingDigits/templates/digit" + str(i) + "_" + str(f) + ".tif", str(i), str(f),
                      "training/", "test/")

#creating training set for letters
i = i + 1
for c in letters:
    for f in range(1,4):
        createSamples("trainingLetters/templates/letter" + c + "_"+str(f)+".tif", str(i),str(f), "training/","test/")
    i = i + 1





