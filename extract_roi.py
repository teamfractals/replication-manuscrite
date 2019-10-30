import cv2
import numpy as np
import os
import sys
from utils import get_filename_list
from PIL import Image

def color_mask(hsv_img, boundaries):
    lower, upper = boundaries

    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")

    # find the colors within the specified boundaries and apply the mask
    mask = cv2.inRange(hsv_img, lower, upper)
    return mask

def extract_roi(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    boundaries = [([0,90,60], [40, 255, 255]),
                  ([150,50,60], [179, 255, 255])] 
    
    mask = np.zeros((hsv.shape[0], hsv.shape[1]), dtype='uint8')
    for b in boundaries:
        m = color_mask(hsv, b)
        mask = cv2.bitwise_or(mask, m)
    
    #cv2.imshow('mask', mask)
    #cv2.waitKey()
    
    xmin, xmax = 100000, 0
    ymin, ymax = 100000, 0
    nonzero_x = cv2.findNonZero(mask)
    nonzero_y = cv2.findNonZero(cv2.transpose(mask))

    if len(nonzero_x) > 0:
        ymin, ymax = nonzero_x[0][0][1], nonzero_x[-1][0][1]
    if len(nonzero_y) > 0:
        xmin, xmax = nonzero_y[0][0][1], nonzero_y[-1][0][1]

    #print(xmin, xmax, ymin, ymax)
    #cv2.rectangle(img,(xmin,ymin),(xmax, ymax),(255,0,0),1)
    #cv2.imshow('rect', img)
    
    roi = img[ymin:ymax, xmin:xmax]
    return roi

def extract_roi_for_dir(box_dir):
    # Setup output dir
    os.makedirs(box_dir+"/roi", exist_ok=True)

    filenames = get_filename_list()

    for name in filenames:
        print("PROCESSING: " + name)
        img = cv2.imread( box_dir + "/" + name)
        roi = extract_roi(img)
        cv2.imwrite(box_dir + "/roi/" + name, roi)
    return

if __name__ == '__main__':
    box_dir = 'out/ideal'
    if len(sys.argv) > 1:
        box_dir = sys.argv[1]
    extract_roi_for_dir(box_dir)
