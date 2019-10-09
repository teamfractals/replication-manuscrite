# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 23:09:54 2019

@author: sharma
"""
from PIL import Image,ImageDraw
from utils import get_filename_dict
import sys
from os.path import join as pathjoin
import os

def generate_layout(text, in_path, out_file):
    PAGE_WIDTH      = 2480
    PAGE_HEIGHT     = 3508
    PAGE_COLOR      = (255, 255, 255)
    MARGIN_LEFT     = 80
    MARGIN_RIGHT    = 80
    MARGIN_TOP      = 240
    LING_SPACING    = 130
    CHAR_SPACING    = 4
    SPACE_REPR      = '_space_'
    SPACE_WIDTH     = 75

    im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    """
    # LINE DRAW
    draw = ImageDraw.Draw(im)
    for i in range(0,3400,80):
        if i%LING_SPACING!=0:
            draw.line((0,i, 3400, i), fill=128, width=5)
    """
    exp_lis = [pathjoin(in_path, 'roi/f_small.png'), 
               pathjoin(in_path, 'roi/g_small.png'), 
               pathjoin(in_path, 'roi/p_small.png'),
               pathjoin(in_path, 'roi/y_small.png'),
               pathjoin(in_path, 'roi/j_small.png'),
               pathjoin(in_path, 'roi/q_small.png')]

    list_im = []
    names = get_filename_dict()
    for i in text:
        if i != ' ':
            list_im.append(pathjoin(in_path, "roi/", names.get(i, 'x_cap.png')))
        else:
            list_im.append(SPACE_REPR)

    list_am = []
    for i in list_im:
        list_am.append(i.replace(os.sep, '/'))

    list_cm = []
    tot = 0
    ind = 0
    ind_n = 0
    tot_curr = 0

    for i in list_am:
        if i == SPACE_REPR:
            ind = ind_n
            tot_curr = tot
            tot += SPACE_WIDTH
            list_cm.append(i)
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                list_am[ind] ="line_break"
                tot = tot - tot_curr
        else:
            im_c = Image.open(i)
            w,h = im_c.size
            tot += w + CHAR_SPACING
            list_cm.append(i)
            print(str(tot)+"\n")
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                tot = tot-tot_curr
                list_am[ind] = "line_break"
        ind_n += 1
        
    print(list_am)
    w_p = MARGIN_LEFT
    h_p = MARGIN_TOP
    for img_name in list_am:    
        if img_name == "line_break":
            w_p = MARGIN_LEFT
            h_p += LING_SPACING
        elif img_name == SPACE_REPR:
            w_p = w_p + SPACE_WIDTH
        else:
            im_c = Image.open(img_name)
            if img_name in exp_lis:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p-54))
            else:
                w,h = im_c.size   
                im.paste(im_c,(w_p,h_p-h))
            w_p = w_p + w+4;
            im.save(pathjoin(out_file))

if __name__ == '__main__':
    text = 'Team Fractals 1234'
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
