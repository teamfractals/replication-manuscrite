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
import os

def generate_layout(text, in_path, out_file):
    names = get_filename_dict()
    mode = 'RGB' # for color image “L” (luminance) for greyscale images, “RGB” for true color images, and “CMYK” for pre-press images.
    size = (2480,3508)
    color = (255, 255, 255)
    names[" "] = "space"
    im = Image.new(mode, size, color)

    line_spacing = 100
    #draw = ImageDraw.Draw(im)
    
    # LINE DRAW
    """
    for i in range(0,3400,80):
        if i%line_spacing!=0:
            draw.line((0,i, 3400, i), fill=128, width=5)
    """
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
    list_am = []
    for i in list_im:
        list_am.append(i.replace(os.sep, '/'))

    list_cm = []
    tot = 0
    ind = 0
    ind_n = 0
    tot_curr = 0
    for i in list_am:
        if i == 'out/sir_scanned/roi/space':
            ind = ind_n
            tot_curr = tot
            tot += 75
            list_cm.append(i)
            if tot > 2320:
                list_am[ind] ="line_break"
                tot = tot - tot_curr
            
            
        else:
            
            im_c = Image.open(i)
            w,h = im_c.size
            tot += w+4
            list_cm.append(i)
            print(str(tot)+"\n")
            if tot > 2320:
                tot = tot-tot_curr
                list_am[ind] = "line_break"
        ind_n += 1
        
    print(list_am)
    w_p = 80
    h_p = 240
    for img_name in list_am:    
        if img_name == "line_break":
            w_p = 80
            h_p += line_spacing
        elif img_name == 'out/sir_scanned/roi/space':
            w_p = w_p + 75
        else:
                
            im_c = Image.open(img_name)
            
            if img_name in exp_lis:
                w,h = im_c.size
                
                im.paste(im_c,(w_p,h_p-54))
        
            else:
                w,h = im_c.size   
                im.paste(im_c,(w_p,h_p-h))
            w_p = w_p + w+4;
            
            im.save(pathjoin(out_file))

if __name__ == '__main__':
    text = 'TeamFractals'
    in_path = 'out/sir'
    out_file = 'out/generated.png'
    if len(sys.argv) > 3:
        text = sys.argv[1]
        in_path = sys.argv[2]
        out_file = sys.argv[3]
    elif len(sys.argv) > 2:
        text = sys.argv[1]
        in_path = sys.argv[2]
    generate_layout(text, in_path, out_file)
