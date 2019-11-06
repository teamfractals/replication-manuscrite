from extract_boxes import extract_boxes
from extract_roi import extract_roi
from layout import generate_layout
import cv2
import os

getinput = input('Do you want to process a new image? (y/n) ')
out_path = 'ERROR'
if getinput.lower() == 'y':
    img_path = input('Input image path: ')
    extract_boxes(img_path)
    img_file = os.path.basename(img_path)
    img_name = img_file[:img_file.find('.')]
    out_path = 'out/' + img_name
    extract_roi(out_path)
else: out_path = input('Output path to use instead: ')

text = input('Text to print out:\n')
generate_layout(text, out_path, 'out/generated.png')

print('DONE')
"""
i = cv2.imread('out/generated.png')
cv2.namedWindow('Output Generated', cv2.WINDOW_NORMAL)
cv2.imshow('Output Generated', i)

cv2.waitKey()
cv2.destroyAllWindows()
"""
