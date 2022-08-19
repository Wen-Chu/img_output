import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import re
import pillow_heif

font_path = r'C:\Windows\Fonts\mingliu.ttc'

def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

def add_word(num, nam, loc, sfname):
        loca = "地點：" + loc
        name = "作者：" + nam
        if sfname[-5:] == '.HEIC':
            heif_file = pillow_heif.read_heif(sfname)
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", )
        else:
            im = cv_imread(sfname)
            cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
        w, h = img.size
        if h > w:
            new_w = int((720 * w) / h)
            new_h = 720
        else:
            new_w = 720
            new_h = int((720 * h) / w)
            if new_h < 350:
                new_w = 1280
                new_h = int((1280 * h) / w)
        img = img.resize((new_w, new_h))
        bg = Image.new('RGB', (new_w, 25), (255, 255, 255))
        draw = ImageDraw.Draw(bg)
        font = ImageFont.truetype(font_path, 16)
        draw.text((10, 4), loca, (0, 0, 0), font=font)
        if re.findall(r'[\u4e00-\u9fff]+', nam):
            draw.text((new_w - (len(name) * 16 + 10), 4), name, (0, 0, 0), font=font)
        else:
            draw.text((new_w - (3 * 16 + (len(name)-3) * 8 + 10), 4), name, (0, 0, 0), font=font)
        combine = Image.new('RGB', (new_w, new_h+25), (250, 250, 250))
        combine.paste(img, (0, 0))
        combine.paste(bg, (0, new_h))
        combine.save(os.path.join(out_path, 'gallery_' + num.zfill(3) +'.jpg'))

path = r'C:\Users\WenChu\Desktop\temp'
out_path = r'C:\Users\WenChu\Desktop\Donee3'
list = os.listdir(path)
for pic in list:
    txt = pic.split('.')[1]
    num = pic.split('.')[0]
    name = txt.split('_')[0]
    loca = txt.split('_')[1]
    print(num, name, loca)
    add_word(num, name, loca, os.path.join(path, pic))