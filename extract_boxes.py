import cv2
import numpy as np
import os
import sys
from utils import get_filename_list

def sort_contours2(cnts, method="left-to-right"):
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b: b[1][1]*15 + b[1][0], reverse=False))
 
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

def extract_boxes(img_path):
    # Setting up directories
    os.makedirs('out', exist_ok=True)
    img_file = os.path.basename(img_path)
    img_name = img_file[:img_file.find('.')]
    os.makedirs('out/'+img_name, exist_ok=True)

    # Read the image
    img = cv2.imread(img_path)
    # grayscaling:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Invert the image
    img_bin = 255 - img_bin
    cv2.imwrite("out/" + img_name + "/" + "threshold_inv.jpg", img_bin)

    # Defining a kernel length
    kernel_length = np.array(img).shape[1]//80
     
    # A verticle kernel of (1 X kernel_length), which will detect all the verticle lines from the image.
    verticle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_length))
    # A horizontal kernel of (kernel_length X 1), which will help to detect all the horizontal line from the image.
    hori_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_length, 1))
    # A kernel of (3 X 3) ones.
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological operation to detect vertical lines from an image
    img_temp1 = cv2.erode(img_bin, verticle_kernel, iterations=3)
    verticle_lines_img = cv2.dilate(img_temp1, verticle_kernel, iterations=3)
    cv2.imwrite("out/" + img_name + "/" + "verticle_lines.jpg",verticle_lines_img)

    # Morphological operation to detect horizontal lines from an image
    img_temp2 = cv2.erode(img_bin, hori_kernel, iterations=3)
    horizontal_lines_img = cv2.dilate(img_temp2, hori_kernel, iterations=3)
    cv2.imwrite("out/" + img_name + "/" + "horizontal_lines.jpg",horizontal_lines_img)

    # Weighting parameters, this will decide the quantity of an image to be added to make a new image.
    alpha = 0.5
    beta = 1.0 - alpha

    # This function helps to add two image with specific weight parameter to get a third image as summation of two image.
    img_final_bin = cv2.addWeighted(verticle_lines_img, alpha, horizontal_lines_img, beta, 0.0)
    img_final_bin = cv2.erode(~img_final_bin, kernel, iterations=2)
    (thresh, img_final_bin) = cv2.threshold(img_final_bin, 128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Find contours for image, which will detect all the boxes
    im2, contours, hierarchy = cv2.findContours(img_final_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Sort all the contours by top to bottom.
    (contours, boundingBoxes) = sort_contours2(contours, method="top-to-bottom")

    img_h = len(img)
    img_w = len(img[0])

    hmin = 0.02 * img_h
    hmax = 0.20 * img_h

    wmin = 0.02 * img_w
    wmax = 0.20 * img_w

    names = get_filename_list()

    idx = 0
    for c in contours:
        # Returns the location and width,height for every contour
        x, y, w, h = cv2.boundingRect(c)

        # If the box height is greater then 20, width is >80, then only save it as a box in "cropped/" folder.
        if (w >= wmin and w <= wmax and h >= hmin and h <= hmax):
            new_img = img[y:y+h, x:x+w]
            print("WRITING: " + img_name + "/" + names[idx])
            cv2.imwrite("out/" + img_name + "/" + names[idx], new_img)
            idx += 1
    return

if __name__=='__main__':
    img_path = 'in/ideal.JPG'
    if len(sys.argv) > 1:
        img_path = sys.argv[1]
    extract_boxes(img_path)

