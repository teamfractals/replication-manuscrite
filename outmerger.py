# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 23:22:45 2019

@author: sharma
"""

import numpy as np
import PIL
from utils import get_filename_dict
import sys

names = get_filename_dict()
inp = input("")
list_im = []
ke = names.keys()
print(ke)
input_dir = "out/kul"
if len(sys.argv) > 1:
    input_dir = sys.argv[1]
for i in inp:
    for j in ke:
        if(i == j):
             list_im.append(input_dir +"/roi/"+ names[j])
for k,v in names.items():
    print(k +"->"+ v)             
print(list_im)

imgs    = [ PIL.Image.open(i) for i in list_im ]
# pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

# save that beautiful picture
imgs_comb = PIL.Image.fromarray( imgs_comb)
imgs_comb.save( input_dir + '/generated.png' )    

