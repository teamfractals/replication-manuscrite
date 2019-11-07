import os
import sys

from PIL import Image, ImageDraw

from page_config import *
from utils import convert_hue, get_filename_dict, img2pdf


def get_char_img_dict(in_path, hue=None, sat=None):
    '''
    Returns a dictionary of Image objects for each character.

    Useful for keeping all the characters available in-memory.
    '''
    filenames = get_filename_dict()
    img_dict = {}
    for char in filenames.keys():
        img_dict[char] = Image.open(os.path.join(in_path, 'roi', filenames[char]))
        if hue is not None or sat is not None:
            img_dict[char] = convert_hue(img_dict[char], hue, sat)
    return img_dict

def generate_layout(text, in_path, out_dir, hue=None, sat=None):
    im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    exp = ['f', 'p', 'j',]
    exp_lis = ['g',  'y', 'q']
    sp_lis_up  = ['*', '^', '“', '”', '‘', '’']
    sp_lis_mid = ['=', ';', '>', '<', '-']
    sp_lis_down = [',']

    img_dict = get_char_img_dict(in_path, hue, sat)
    tot = 0
    ind_n = 0
    char_list = list(text)
    DEFAULT_IMG = img_dict['~']

    count1, count2 = 0, 0
    for i, char in enumerate(text):
        if (char == '"' and count1 == 0):
            char_list[i] = '“'
            count1 = 1
        elif (char == '"' and count1 == 1) :
            char_list[i] = '”'
            count1 = 0
        elif (char == "'" and count2 == 0):
            char_list[i] = '‘'
            count2 = 1
        elif (char == "'" and count2 == 1):
            char_list[i] = '’'
            count2 = 0


    for char in char_list:
          if char == '\n' or char == '\r':
              tot = MARGIN_LEFT
          elif char == ' ':
            tot += SPACE_WIDTH
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                char_list.insert(ind_n, 'line_break')
                if(char_list[ind_n+1] == ' '):
                    del([char_list[ind_n+1]])
                if(char_list[ind_n-1] == ' '):
                    del([char_list[ind_n-1]])    
                tot = MARGIN_LEFT
          elif char != "line_break":
            w, h = img_dict.get(char, DEFAULT_IMG).size
            tot += w + CHAR_SPACING
            if tot > (PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT):
                tot = MARGIN_LEFT
                char_list.insert(ind_n,"line_break")
                if(char_list[ind_n-1] == ' '):
                    del([char_list[ind_n-1]])
                else:
                    char_list.insert(ind_n, '-')
                if(char_list[ind_n+1] == ' '):
                    del([char_list[ind_n+1]])
          ind_n += 1

    i = 0
    w_p = MARGIN_LEFT
    h_p = MARGIN_TOP
    
    os.makedirs(out_dir, exist_ok=True)
    path_list = []
    page_cnt = 0

    for i, char in enumerate(char_list):    
        if char == "line_break":
            w_p = MARGIN_LEFT
            h_p += LING_SPACING
        elif char == '\r' or char == '\n':
            if char == '\n':
                # handle Windows line endings
                if i-1 > 0 and char_list[i-1] == '\r':
                    continue
            w_p = MARGIN_LEFT
            h_p += LING_SPACING    
        elif char == ' ':
            w_p = w_p + SPACE_WIDTH
        else:
            im_c = img_dict.get(char, DEFAULT_IMG)
            if char in exp_lis:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p - EXP_FIX))
            elif char in sp_lis_up:
                w,h = im_c.size
                im.paste(im_c,(w_p, h_p - EXP_TOP))
            elif char in sp_lis_mid:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_MID ))
            elif char in sp_lis_down:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_BOTTOM))
            elif char in exp:
                w,h = im_c.size
                im.paste(im_c,(w_p,h_p - EXP_EXP))    
            else:
                w,h = im_c.size   
                im.paste(im_c,(w_p,h_p-h))
            w_p = w_p + w + CHAR_SPACING;
        if h_p >= PAGE_HEIGHT - MARGIN_BOTTOM:
            w_p = MARGIN_LEFT
            h_p = MARGIN_TOP   
            save_path = os.path.join(out_dir, str(page_cnt) + ".png")
            im.save(save_path)
            page_cnt += 1
            print('Saved page', page_cnt, '...')
            path_list.append(save_path)
            i += 1
            im = Image.new('RGB', (PAGE_WIDTH, PAGE_HEIGHT), PAGE_COLOR)
    save_path = os.path.join(out_dir, str(page_cnt) + ".png")
    im.save(save_path)     
    page_cnt += 1
    print('Saved page', page_cnt, '...')
    path_list.append(save_path)
    img2pdf(path_list=path_list, out_dir=out_dir)
    print('PDF generated!')
    return len(path_list)
    
if __name__ == '__main__':
    text = "a=b, a = 'b * c', 'hostel' a^b, a-b,"
    in_path = 'out/siddhu_allchars_crop'
    out_dir = 'out/__generated__'
    if len(sys.argv) > 3:
        text = sys.argv[1]
        in_path = sys.argv[2]
        out_dir = sys.argv[3]
    elif len(sys.argv) > 2:
        text = sys.argv[1]
        in_path = sys.argv[2]
    generate_layout(text, in_path, out_dir)
