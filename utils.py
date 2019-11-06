from PIL import Image
import os

def get_filename_dict():
    filenames = {}
    for a in range(26):
        filenames[chr(a+65)] = chr(97 + a) + "_cap.png"
    for a in range(26):
        filenames[chr(a+97)] = chr(97 + a) + "_small.png"
    for a in range(10):
        filenames[chr(a+48)] = chr(48 + a) + ".png"
    filenames['!']="11_exclamation.png"
    filenames['$']="12_dollar.png"
    filenames['&']="13_ampersand.png"
    filenames['(']="14_left_parenthesis.png"
    filenames[')']="15_right_parenthesis.png"
    filenames['{']="16_left_brace.png"
    filenames['}']="17_right_brace.png"
    filenames['[']="18_left_bracket.png"
    filenames[']']="19_right_bracket.png"
    filenames['-']="20_minus.png"
    filenames['+']="21_plus.png"
    filenames['_']="22_underscore.png"
    filenames[';']="23_semi_colon.png"
    filenames[':']="24_colon.png"
    filenames[',']="25_comma.png"
    filenames['.']="26_full_stop.png"
    filenames['?']="27_question_mark.png"
    filenames['“']="28_open_double_quote.png"
    filenames['”']="29_close_double_quote.png"
    filenames['‘']="30_open_single_quote.png"
    filenames['’']="31_close_single_quote.png"
    filenames['%']="32_percent.png"
    filenames['#']="33_hash.png"
    filenames['*']="34_asterisk.png"
    filenames['~']="35_tilde.png"
    filenames['/']="36_front_slash.png"
    filenames['|']="37_vertical_bar.png"
    filenames['\\']="38_back_slash.png"
    filenames['>']="39_greater_than.png"
    filenames['<']="40_less_than.png"
    filenames['=']="41_equal.png"
    filenames['@']="42_at_the_rate.png"
    filenames['^']="43_caret.png"
    
    
    return filenames

def get_filename_list():
    filenames = []
    for a in range(26):
        filenames.append(chr(97 + a) + "_cap.png")
    for a in range(26):
        filenames.append(chr(97 + a) + "_small.png")
    for a in range(10):
        filenames.append(chr(48 + a) + ".png")
    filenames.append("11_exclamation.png")
    filenames.append("12_dollar.png")
    filenames.append("13_ampersand.png")
    filenames.append("14_left_parenthesis.png")
    filenames.append("15_right_parenthesis.png")
    filenames.append("16_left_brace.png")
    filenames.append("17_right_brace.png")
    filenames.append("18_left_bracket.png")
    filenames.append("19_right_bracket.png")
    filenames.append("20_minus.png")
    filenames.append("21_plus.png")
    filenames.append("22_underscore.png")
    filenames.append("23_semi_colon.png")
    filenames.append("24_colon.png")
    filenames.append("25_comma.png")
    filenames.append("26_full_stop.png")
    filenames.append("27_question_mark.png")
    filenames.append("28_open_double_quote.png")
    filenames.append("29_close_double_quote.png")
    filenames.append("30_open_single_quote.png")
    filenames.append("31_close_single_quote.png")
    filenames.append("32_percent.png")
    filenames.append("33_hash.png")
    filenames.append("34_asterisk.png")
    filenames.append("35_tilde.png")
    filenames.append("36_front_slash.png")
    filenames.append("37_vertical_bar.png")
    filenames.append("38_back_slash.png")
    filenames.append("39_greater_than.png")
    filenames.append("40_less_than.png")
    filenames.append("41_equal.png")
    filenames.append("42_at_the_rate.png")
    filenames.append("43_caret.png")
    return filenames

def img2pdf(img_list=None, path_list=None, out_dir="out"):
    generated_pdf = os.path.join(out_dir, "generated.pdf")
    if img_list is None:
        img_list = [Image.open(path) for path in path_list]
    img_list[0].save(generated_pdf, "PDF", resolution = 100.0, save_all = True, append_images = img_list[1:])

