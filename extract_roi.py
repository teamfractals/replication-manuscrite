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

def extract_roi(box_dir):
    # Setup output dir
    os.makedirs(box_dir+"/roi", exist_ok=True)

    filenames = get_filename_list()

    for name in filenames:
        print("READING: " + box_dir + "/" + name)
        img = cv2.imread( box_dir + "/" + name)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        boundaries = [([0,50,60], [40, 255, 255]),
                      ([135,50,60], [179, 255, 255])] 
        
        mask = np.zeros((hsv.shape[0], hsv.shape[1]), dtype='uint8')
        for b in boundaries:
            m = color_mask(hsv, b)
            mask = cv2.bitwise_or(mask, m)
        
        #cv2.imshow('mask', mask)
        #cv2.waitKey()
        
        xmin, xmax = 100000, 0
        ymin, ymax = 100000, 0
        
        i = 0
        while i < mask.shape[0]:
            j = 0
            while j < mask.shape[1]:
                if mask[i][j] != 0:
                    if j < xmin: xmin = j
                    if j > xmax: xmax = j
                    if i < ymin: ymin = i
                    if i > ymax: ymax = i
                j += 1
            i += 1
        
        #print(xmin, xmax, ymin, ymax)
        #cv2.rectangle(img,(xmin,ymin),(xmax, ymax),(255,0,0),1)
        #cv2.imshow('rect', img)
        
        roi = img[ymin:ymax, xmin:xmax]
        cv2.imwrite(box_dir + "/roi/" + name, roi)
        
        """
        img = Image.open(box_dir + "/roi/" + name)

        ary = np.array(img)
        
        # Split the three channels
        r,g,b = np.split(ary,3,axis=2)
        r=r.reshape(-1)
        g=r.reshape(-1)
        b=r.reshape(-1)
        
        # Standard RGB to grayscale 
        #bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2], zip(r,g,b)))
        
        bitmap = list(map(lambda x: 0.01*x[0]+0.10*x[1]+0.50*x[2], zip(r,g,b)))
        bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
        bitmap = np.dot((bitmap > 128).astype(float),255)
        im = Image.fromarray(bitmap.astype(np.uint8))
        
        im.save(box_dir + "/roi/" + name)
        
        """
        
    return

if __name__ == '__main__':
    box_dir = 'out/ideal'
    if len(sys.argv) > 1:
        box_dir = sys.argv[1]
    extract_roi(box_dir)
