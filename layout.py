# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 23:09:54 2019

@author: sharma
"""
'''
import numpy as np
img = np.zeros([100,100,3],dtype=np.uint8)
img.fill(255) 
'''

from PIL import Image,ImageDraw
from utils import get_filename_dict
import sys
from os.path import join as pathjoin

def generate_layout(text, in_path, out_file):
    names = get_filename_dict()
    mode = 'RGB' # for color image “L” (luminance) for greyscale images, “RGB” for true color images, and “CMYK” for pre-press images.
    size = (2480,3508)
    color = (255, 255, 255)

    im = Image.new(mode, size, color)

    draw = ImageDraw.Draw(im)
    for i in range(0,3400,80):
        if i%320!=0:
            draw.line((0,i, 3400, i), fill=128, width=5)

    exp_lis = [pathjoin(in_path, 'roi/f_small.png'), 
               pathjoin(in_path, 'roi/g_small.png'), 
               pathjoin(in_path, 'roi/p_small.png'),
               pathjoin(in_path, 'roi/y_small.png'),
               pathjoin(in_path, 'roi/j_small.png'),
               pathjoin(in_path, 'roi/q_small.png')]
    list_im = []

    ke = names.keys()    
    for i in text:
        for j in ke:
            if(i == j):
                 list_im.append(pathjoin(in_path, "roi/", names[j]))
        
    w_p = 0    
    for img_name in list_im:    
        im_c = Image.open(img_name)
        
        if img_name in exp_lis:
            w,h = im_c.size   
            im.paste(im_c,(w_p,160))
        else:
            w,h = im_c.size   
            im.paste(im_c,(w_p,240-h))
        w_p = w_p + w;
        im.save(pathjoin(out_file))

if __name__ == '__main__':
    in_path = 'out/sir'
    if len(sys.argv) > 1:
        in_path = sys.argv[1]
    generate_layout(in_path)
