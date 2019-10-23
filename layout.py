from PIL import Image,ImageDraw
from utils import get_filename_dict
import sys
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
    EXP_FIX         = 35
    EXP_MID         = 37
    EXP_TOP         = 54
    EXP_BOTTOM      = 11
    EXP_EXP         = 54

    im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    '''
    # LINE DRAW
    draw = ImageDraw.Draw(im)
    for i in range(0,3400,80):
        if i%LING_SPACING!=0:
            draw.line((0,i, 3400, i), fill=128, width=2)
    '''        
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
    for i in text:
        if i != ' ':
            file_list.append(names.get(i, '8.png'))
        else:
            file_list.append(SPACE_REPR)
    tot = 0
    ind_n = 0
    tot_curr = 0

    for i in file_list:
        if i == SPACE_REPR:
            print("hey")
            tot_curr = tot
            tot += SPACE_WIDTH
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                
                
                file_list.insert(ind_n,"line_break")
               
                if(file_list[ind_n+1] == SPACE_REPR):
                    del([file_list[ind_n+1]])
                if(file_list[ind_n-1] == SPACE_REPR):
                    del([file_list[ind_n-1]])    
                #tot = tot - tot_curr
                tot =  MARGIN_LEFT
        else:
            im_c = Image.open(os.path.normpath(os.path.join(in_path, 'roi', i)))
            w, h = im_c.size
            tot += w + CHAR_SPACING
            print(str(tot)+"\n")
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                
                tot = MARGIN_LEFT
                
                file_list.insert(ind_n,"line_break")
                
                if(file_list[ind_n+1] == SPACE_REPR):
                    del([file_list[ind_n+1]])
                #if(file_list[ind_n-1] != SPACE_REPR):
                #   file_list.insert(ind_n-1,"20_minus.png")
                if(file_list[ind_n-1] == SPACE_REPR):
                    del([file_list[ind_n-1]])
                print(file_list[ind_n])    
                
        ind_n += 1
        
    print(file_list)
    w_p = MARGIN_LEFT
    h_p = MARGIN_TOP
    for img_name in file_list:    
        if img_name == "line_break":
            w_p = MARGIN_LEFT
            h_p += LING_SPACING
        elif img_name == SPACE_REPR:
            w_p = w_p + SPACE_WIDTH
        else:
            im_c = Image.open(os.path.normpath(os.path.join(in_path, 'roi', img_name)))
            if img_name in exp_lis:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p-EXP_FIX))
            elif img_name in sp_lis_up:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p-EXP_TOP))
            elif img_name in sp_lis_mid:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p -EXP_MID ))
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
    im.save(os.path.normpath(out_file))
              
        
    
if __name__ == '__main__':
    text = "a=b, a = 'b * c', 'hell yeah' a^b, a-b,"
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
