

import cv2


for i in range(1,23,1):
    for j in range(3):
        filenameSource = "singleCharsSource/char" + str(i) + "_" + str(j) + ".tif"
        filename = "singleChars/char" + str(i) + "_" + str(j) + ".tif"
        img = cv2.imread(filenameSource)
        img = cv2.copyMakeBorder(img, 2, 2, 2, 2, cv2.BORDER_REPLICATE)
        cv2.imwrite(filename, img)