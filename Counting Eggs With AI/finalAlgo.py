import numpy as np
import cv2
import math
import os
import sys

# function that rejects outliers from a numpy array and returns that array without outliers
# obtained from stack overflow: https://stackoverflow.com/questions/11686720/is-there-a-numpy-builtin-to-reject-outliers-from-a-list
def reject_outliers(data, m = 2.):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<m]

# for every file name in command line, find the number of eggs in the image
for arg in range(1, len(sys.argv)):
    # ensure file name exists and is imported corectly
    try:
        FILENAME = str(sys.argv[arg])
        img = cv2.imread(FILENAME)
        lower_black = np.array([0, 0, 0], dtype="uint16")
        upper_black = np.array([100, 100, 100], dtype="uint16")
        img2 = img
        tempImg = cv2.imread(FILENAME)
        gray = cv2.cvtColor(tempImg, cv2.COLOR_RGB2GRAY)
    except: 
        print("Invalid file name: " + str(sys.argv[arg]) + ", aborting program\n")
        exit(0)
    
    cv2.imwrite("gray.jpg", gray)
    frame = cv2.imread("gray.jpg")
    try: 
            os.remove("gray.jpg")
    except: pass
    black_mask = cv2.inRange(frame, lower_black, upper_black)
    canny = black_mask
    canny = cv2.GaussianBlur(black_mask, (11, 11), 0)
    dilated = cv2.dilate(canny, (1, 1), iterations=1)
    (contours, heirarchy) = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
    cv2.drawContours(rgb, contours, -1, (0, 255, 0), 2)

    # calculate average area of single egg
    contArray = []

    # get array of areas
    for i in contours:
        area = math.floor(cv2.contourArea(i))
        contArray.append(area)
    contArray.sort()
    contArray = np.array(contArray)
    contArray = reject_outliers(contArray)
    contArray = reject_outliers(contArray)
    contArray = reject_outliers(contArray)

    # assertion: average area is median of array without outliers
    EGG_AREA = np.median(contArray)

    # NEXT STEP - CALCULATE COUNT
    # assuming EGG_AREA is the area of one egg, and count is number of eggs
    count = 0;
    for i in contours:
        area = cv2.contourArea(i)
        if(area > EGG_AREA+(EGG_AREA*.4)):
            count += math.floor(area/(EGG_AREA-(EGG_AREA*.18)))
        elif(area > EGG_AREA-(EGG_AREA*.4)):
            count += 1


    print("Number of eggs in file " + str(sys.argv[arg]) + ": " + str(count));

