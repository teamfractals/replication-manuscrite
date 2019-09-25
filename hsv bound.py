import cv2
import numpy as np

names3 = ["adi","prj","sid","ideal","ideal_large","kul"]
input_name = names3[5]


names1 = []
for a in range(26):
    names1.append(chr(97 + a)+"_cap")
for a in range(26):
    names1.append(chr(97 + a)+"_small")
for a in range(10):
    names1.append(chr(48 + a))

names2 = []
for a in range(26):
    names2.append(chr(97 + a)+"_cap_roi")
for a in range(26):
    names2.append(chr(97 + a)+"_small_roi")
for a in range(10):
    names2.append(chr(48 + a)+ "_roi")


count = 0
for alpha in names1:
    img = cv2.imread("out/" + input_name  +"/" + str(alpha) + ".png")
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    boundaries = [([0,80,80], [40, 255, 255]),
                  ([135,80,80], [179, 255, 255])] 
    
    def color_mask(hsv_img, boundaries):
        lower, upper = boundaries
        # create NumPy arrays from the boundaries
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
    
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(hsv_img, lower, upper)
        #cv2.imshow('mask', mask)
        #cv2.waitKey()
        #output = cv2.bitwise_and(img, img, mask = mask)
        return mask
    
    mask = np.zeros((hsv.shape[0], hsv.shape[1]), dtype='uint8')
    #print(mask.shape)
    
    for b in boundaries:
        m = color_mask(hsv, b)
        #print(m.shape)
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
    cv2.imwrite("out/" + input_name + "/roi/"+ str(names2[count])+ ".png", roi)
    count += 1

cv2.waitKey()
cv2.destroyAllWindows()
