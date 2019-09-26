def get_filename_dict():
    filenames = {}
    for a in range(26):
        filenames[chr(a+65)] = chr(97 + a) + "_cap.png"
    for a in range(26):
        filenames[chr(a+97)] = chr(97 + a) + "_small.png"
    for a in range(10):
        filenames[chr(a+48)] = chr(48 + a) + ".png"
    return filenames

def get_filename_list():
    filenames = []
    for a in range(26):
        filenames.append(chr(97 + a) + "_cap.png")
    for a in range(26):
        filenames.append(chr(97 + a) + "_small.png")
    for a in range(10):
        filenames.append(chr(48 + a) + ".png")
    return filenames
    
