from extract_boxes import extract_boxes
from extract_roi import extract_roi_for_dir
from layout import generate_layout
import cv2
import os
import sys

infile = None
if len(sys.argv) > 1:
    infile = sys.argv[1]

getinput = input('Do you want to process a new image? (y/n) ')
out_path = 'ERROR'
if getinput.lower() == 'y':
    img_path = input('Input image path: ')
    extract_boxes(img_path)
    img_file = os.path.basename(img_path)
    img_name = img_file[:img_file.find('.')]
    out_path = 'out/' + img_name
    extract_roi_for_dir(out_path)
else: out_path = input('Output path to use instead: ')

if infile is None:
    text = input('Text to print out:\n')
else:
    with open(infile, 'r',encoding = "utf8") as f:
        text = f.read()

hue = None
if input('Do you want to specify a new hue? (y/n) ').lower() == 'y':
    hue = int(input('Enter hue (0-179): '))

sat = None
if input('Do you want to specify a new saturation? (y/n) ').lower() == 'y':
    sat = int(input('Enter sat (0-255): '))

generate_layout(text, out_path, 'out/__generated__', hue, sat)
print('DONE')
