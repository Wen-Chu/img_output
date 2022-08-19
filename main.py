import cv2
import numpy as np
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import re
import pillow_heif

win = tk.Tk()
win.title('Gallery')
win.geometry('280x300')
canvas = tk.Canvas(win, width=280, height=300)
canvas.pack()
font_path = r'C:\Windows\Fonts\mingliu.ttc'

def reset():
    btn_gen['state'] = tk.DISABLED
    btn_pic['state'] = tk.NORMAL
    btn_pic['text'] = '選擇本機圖片'
    textbox_loca.delete("1.0", "end")
    textbox_name.delete("1.0", "end")

def save_file(img):
    save_path = filedialog.asksaveasfile(defaultextension=("jpg", "*.jpg"), filetype=(("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png")))
    img.save(save_path.name)
    reset()

def cv_imread(filePath):
    cv_img = cv2.imdecode(np.fromfile(filePath, dtype=np.uint8), -1)
    return cv_img

def choice_img():
    global sfname
    sfname = filedialog.askopenfilename(title='選擇圖片', filetype=(("jpg", "*.jpg"), ("jpeg", "*.jpeg"), ("png", "*.png"), ("HEIC", "*.HEIC")))
    if sfname:
        btn_pic['state'] = tk.DISABLED
        btn_pic['text'] = '圖片已選擇'
        btn_gen['state'] = tk.NORMAL

def add_word():
    if textbox_loca.get("1.0", "end-1c") == '' or textbox_name.get("1.0", "end-1c") == '':
        lable_warn['text'] = "地點或作者尚未填寫！"
    else:
        loca = "地點：" + textbox_loca.get("1.0", "end-1c")
        name = "作者：" + textbox_name.get("1.0", "end-1c")
        if sfname[-5:] == '.HEIC':
            heif_file = pillow_heif.read_heif(sfname)
            img = Image.frombytes(heif_file.mode, heif_file.size, heif_file.data, "raw", )
        else:
            im = cv_imread(sfname)
            cv2image = cv2.cvtColor(im, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
        if radioValue.get() == 1:
            img = img.rotate(270, expand=True)
        elif radioValue.get() == 2:
            img = img.rotate(180, expand=True)
        elif radioValue.get() == 3:
            img = img.rotate(90, expand=True)
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
        if re.findall(r'[\u4e00-\u9fff]+', textbox_name.get("1.0", "end-1c")):
            draw.text((new_w - (len(name) * 16 + 10), 4), name, (0, 0, 0), font=font)
        else:
            draw.text((new_w - (3 * 16 + (len(name)-3) * (16/2) + 10), 4), name, (0, 0, 0), font=font)
        combine = Image.new('RGB', (new_w, new_h+25), (250, 250, 250))
        combine.paste(img, (0, 0))
        combine.paste(bg, (0, new_h))
        save_file(combine)

lable_loca = tk.Label(canvas, text="地點：", height=2)
lable_loca.grid(column=0, row=0, sticky='W')
textbox_loca = tk.Text(canvas, height=1, width=15)
textbox_loca.grid(column=1, row=0, sticky='W')
lable_name = tk.Label(canvas, text="作者：", height=2)
lable_name.grid(column=0, row=1, sticky='W')
textbox_name = tk.Text(canvas, height=1, width=15)
textbox_name.grid(column=1, row=1, sticky='W')
lable_pic = tk.Label(canvas, text="圖片：", height=2)
lable_pic.grid(column=0, row=2, sticky='W')
btn_pic = tk.Button(canvas, text="選擇本機圖片", command=choice_img)
btn_pic.grid(column=1, row=2, sticky='W')
radioValue = tk.IntVar()
btn_rota1 = tk.Radiobutton(canvas, text="圖片方向不變", variable=radioValue, value=0)
btn_rota1.select()
btn_rota1.grid(column=1, row=3, sticky='W')
btn_rota2 = tk.Radiobutton(canvas, text="圖片向右旋轉90度", variable=radioValue, value=1)
btn_rota2.grid(column=1, row=4, sticky='W')
btn_rota3 = tk.Radiobutton(canvas, text="圖片旋轉180度", variable=radioValue, value=2)
btn_rota3.grid(column=1, row=5, sticky='W')
btn_rota4 = tk.Radiobutton(canvas, text="圖片向左旋轉90度", variable=radioValue, value=3)
btn_rota4.grid(column=1, row=6, sticky='W')
btn_gen = tk.Button(canvas, text="生成", command=add_word, state=tk.DISABLED)
btn_gen.grid(column=1, row=7, sticky='W')
btn_re = tk.Button(canvas, text="重新製作", command=reset)
btn_re.grid(column=1, row=8, sticky='W')
lable_warn = tk.Label(canvas, text='', height=2, fg='#EE4B2B')
lable_warn.grid(column=1, row=9, sticky='W')
win.mainloop()