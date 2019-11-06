from PIL import Image,ImageDraw
from utils import get_filename_dict
from utils import img2pdf
from page_config import *
import sys
import os

def generate_layout(text, in_path, out_dir):
    im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    exp = ['f_small.png',
           'p_small.png',
           'j_small.png',
           ]
    exp_lis = [ 
               'g_small.png', 
               'y_small.png',
               'q_small.png']
    sp_lis_up  = ['34_asterisk.png',
                  '43_caret.png',
                  '28_open_double_quote.png',
                  '29_close_double_quote.png',
                  '30_open_single_quote.png',
                  '31_close_single_quote.png'
                  ]
    sp_lis_mid = ['41_equal.png',
                  '23_semi_colon.png',
                  '39_greater_than.png',
                  '40_less_than.png']
    sp_lis_down = ['25_comma.png']

    file_list = []
    names = get_filename_dict()
    count1 = 0
    count2 = 0
    print("controlB")
    for i in text:
        if ( i == '"' and count1 == 0 ):
            file_list.append(names.get(i,"28_open_double_quote.png"))
            count1 = 1
        elif (i == '"' and count1 == 1 ) :
            file_list.append(names.get(i,"29_close_double_quote.png"))
            count1 = 0
        elif ( i == "'" and count2 == 0 ):
            file_list.append(names.get(i,"30_open_single_quote.png"))
            count2 = 1
        elif (i == "'" and count2 == 1):
            file_list.append(names.get(i,"31_close_single_quote.png"))
            count2 = 0
        elif i == "\r" or i == "\n":
            print("found it\n")
            file_list.append("EnterKey")
        elif i != ' ':
            file_list.append(names.get(i, '8.png'))
        else:
            file_list.append(SPACE_REPR)
    tot = 0
    ind_n = 0
    print("controlC")
    for i in file_list:
          if i == "EnterKey":
              tot = MARGIN_LEFT
          elif i == SPACE_REPR:
            print("hey")
            
            tot += SPACE_WIDTH
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                file_list.insert(ind_n,"line_break")
                if(file_list[ind_n+1] == SPACE_REPR):
                    del([file_list[ind_n+1]])
                if(file_list[ind_n-1] == SPACE_REPR):
                    del([file_list[ind_n-1]])    
                tot = MARGIN_LEFT
          elif i != "line_break":
            im_c = Image.open(os.path.normpath(os.path.join(in_path, 'roi', i)))
            w, h = im_c.size
            tot += w + CHAR_SPACING
            print(str(tot)+"\n")
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                tot = MARGIN_LEFT
                file_list.insert(ind_n,"line_break")
                if(file_list[ind_n-1] == SPACE_REPR):
                    del([file_list[ind_n-1]])
                else:
                    file_list.insert(ind_n,"20_minus.png")
                if(file_list[ind_n+1] == SPACE_REPR):
                    del([file_list[ind_n+1]])
                #if(file_list[ind_n-1] != SPACE_REPR):
                #   file_list.insert(ind_n-1,"20_minus.png")
                print(file_list[ind_n])    
          ind_n += 1

    print("controlD") 
    print(file_list)
    i = 0
    w_p = MARGIN_LEFT
    h_p = MARGIN_TOP
    
    os.makedirs(out_dir, exist_ok=True)
    path_list = []

    for img_name in file_list:    
        if img_name == "line_break":
            w_p = MARGIN_LEFT
            h_p += LING_SPACING
            
        elif img_name == "EnterKey":
            w_p = MARGIN_LEFT
            h_p += LING_SPACING    
        elif img_name == SPACE_REPR:
            w_p = w_p + SPACE_WIDTH
            
        else:
            im_c = Image.open(os.path.normpath(os.path.join(in_path, 'roi', img_name)))
            if img_name in exp_lis:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p - EXP_FIX))
            elif img_name in sp_lis_up:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p - EXP_TOP))
            elif img_name in sp_lis_mid:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_MID ))
            elif img_name in sp_lis_down:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_BOTTOM))
            elif img_name in exp:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_EXP))    
            else:
                w,h = im_c.size   
                im.paste(im_c,(w_p,h_p-h))
            w_p = w_p + w + CHAR_SPACING;
        if h_p >= PAGE_HEIGHT - MARGIN_BOTTOM:
            w_p = MARGIN_LEFT
            h_p = MARGIN_TOP   
            save_path = os.path.join(out_dir, str(i) + ".png")
            im.save(save_path)
            path_list.append(save_path)
            i += 1
            im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    save_path = os.path.join(out_dir, str(i) + ".png")
    im.save(save_path)     
    path_list.append(save_path)
    img2pdf(path_list=path_list, out_dir=out_dir)
    
if __name__ == '__main__':
    text = "a=b, a = 'b * c', 'hostel' a^b, a-b,"
    in_path = 'out/sir'
    out_dir = 'out/generated'
    if len(sys.argv) > 3:
        text = sys.argv[1]
        in_path = sys.argv[2]
        out_dir = sys.argv[3]
    elif len(sys.argv) > 2:
        text = sys.argv[1]
        in_path = sys.argv[2]
    generate_layout(text, in_path, out_dir)
