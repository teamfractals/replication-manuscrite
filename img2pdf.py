# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 00:59:42 2019

@author: SIDDHARTH AGRAWAL
"""

from PIL import Image

img1 = Image.open("out/generated.png")
#img2 = Image.open("out/filled_template.jpg")

#img_list = [img2]

generated_pdf = "out/generated_blank.pdf"


img1.save(generated_pdf,"PDF",resolution = 100.0 ,save_all = True)#,append_images = img_list)