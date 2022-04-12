# @file gui.py
# @author Kuan-Di Jiang
# @brief Program interface

import os
import tkinter as tk
from tkinter import Label, ttk
from tkinter import font
from tkinter.constants import BOTTOM, LEFT, NW, TOP, X
from PIL import Image,ImageTk
from matplotlib.pyplot import fill, flag, text
from market import GetAvgPrice, GetKline, GetKline_future, drawklineticker
import time
import pandas as pd
import requests #for line notify
def create_label(txt):
    lbl_1 = tk.Label(window, text=txt, bg='yellow', fg='#263238', font=('Arial', 12), width=100, height=1)#宣告一個標籤
    lbl_1.grid(column=0, row=0)#設定放置的位置(grid布局)

def create_button(txt):
    bt_1 = tk.Button(window, text=txt, bg='red', fg='white', font=('Arial', 12))
    bt_1['width'] = 50
    bt_1['height'] = 4
    bt_1['activebackground'] = 'red' #按鈕被按下的背景顏色
    bt_1['activeforeground'] = 'yellow'  #按鈕被暗下的文字顏色(前景)
    bt_1.grid(column=0, row=0)  #位置

def create_label_image(imginput,colin,rowin,img_size,columnspanin,rowspanin,padxin,stickyin):   #columnspan rowspan →default = 1
    img = Image.open(imginput)   #讀取圖片
    img = img.resize((img_size,img_size))    #圖片大小
    imgTk = ImageTk.PhotoImage(img) #轉換成Tkinter可用的圖片
    lbl_2 = tk.Label(window , image=imgTk)  #宣告標籤並設定圖片
    
    lbl_2.image = imgTk     #排版位置
    lbl_2.grid(column=colin,row=rowin,columnspan=columnspanin,rowspan=rowspanin,padx=padxin,sticky=stickyin) 
    return lbl_2
def convert_img_to_tkimg(img,width,height):
    img_bt = Image.open(img)        
    img_bt = ImageTk.PhotoImage(img_bt.resize((width,height)))
    return img_bt
#定義 grid 引入obj為UI widget(小部件) cols 該widget有幾欄 row該widget有幾列     https://www.rs-online.com/designspark/python-tkinter-cn
def define_layout(obj, cols=1, rows=1):
    
    def method(trg, col, row):
        
        for c in range(cols):    
            trg.columnconfigure(c, weight=1)
        for r in range(rows):
            trg.rowconfigure(r, weight=1)

    if type(obj)==list:        
        [ method(trg, cols, rows) for trg in obj ]
    else:
        trg = obj
        method(trg, cols, rows)
def get_size(self, event, obj=''):

    trg_obj = self.window if obj == '' else obj
    self.w, self.h = trg_obj.winfo_width(), trg_obj.winfo_height()
    print(f'\r{(self.w, self.h)}', end='')

def bt1_windows_seperation(img,def_coin,def_time):
    #global  img_size
    global imTK_1, combo1 ,combo1_time, bt_label,price_label1
    bt_label = 1 
    imTK_1 = ImageTk.PhotoImage(img.resize((int(img_size),int(img_size))))
    div1 = tk.Frame(window,  width=img_size , height=img_size )
    div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=100, columnspan=100 , sticky=align_mode)
    image_main = tk.Label(div1,image=imTK_1)      #把圖片放在div1
    image_main.grid(column=0, row=0, sticky= align_mode)

    combo1 = ttk.Combobox(div1,values=coin_list,width= 8)
    combo1.grid(column=0,row=0,sticky=tk.N+tk.W)
    combo1.current(def_coin)
    combo1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_time = ttk.Combobox(div1, values=time_list,width=5)
    combo1_time.current(def_time)
    combo1_time.place(x=80,y=0)
    combo1_time.bind("<<ComboboxSelected>>", choose_token_function)
    try:    #fix initial error (mutual try)
        price_label1 = tk.Label(div1, text=round(price_dataframe.at['price',combo1.get()],2),bg='gray',font=('Arial',15))
        price_label1.place(x=600,y=0)
    except:
        pass
    
    #combo1_time.grid(column=1,row=0,sticky=tk.N+tk.W)
def bt2_windows_seperation(img_1,img_2,def_coin1,def_time1,def_coin2,def_time2):
    global imTK_1 , imTK_2, combo1_1, combo1_2, combo1_1_time, combo1_2_time,bt_label,price_label1_1,price_label1_2

    bt_label = 2
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size/2,height=img_size/2)
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2)
    div1_1.grid(column=0, row=0, rowspan=100, sticky=align_mode)
    div1_2.grid(column=50, row=0, rowspan=100, sticky=align_mode)

    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_1.place(x=0,y=img_size/4) #利用expand=1自動擴展來達成垂直置中
    image_main_2.place(x=0,y=img_size/4)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=0,y=img_size/4)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=img_size/4)
    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=80,y=img_size/4)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=img_size/4)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=250,y=img_size/4)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=img_size/4)

def bt3_windows_seperation(img_1,img_2,def_coin1,def_time1,def_coin2,def_time2):
    global imTK_1 , imTK_2, combo1_1,combo1_2, combo1_1_time, combo1_2_time,bt_label,price_label1_1,price_label1_2
    bt_label = 3
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))

    div1_1 = tk.Frame(window,width= img_size,height=img_size/2,bg='blue')
    div1_2 = tk.Frame(window,width= img_size,height=img_size/2,bg='orange')
    div1_1.grid(column=0, row=0,rowspan=50,columnspan=100,  sticky=align_mode)
    div1_2.grid(column=0, row=50,rowspan=50,columnspan=100, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_1.place(x=img_size/4,y=0) #利用expand=1自動擴展來達成垂直置中
    image_main_2.place(x=img_size/4,y=0)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=img_size/4,y=0)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=img_size/4,y=0)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=img_size/4+80,y=0)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=img_size/4+80,y=0)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=img_size/4+250,y=0)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=img_size/4+250,y=0)
def bt4_windows_seperation(img_1,img_2,img_3,img_4,def_coin1,def_time1,def_coin2,def_time2,def_coin3,def_time3,def_coin4,def_time4):
    global imTK_1 , imTK_2, imTK_3, imTK_4,combo1_1,combo1_2,combo1_3,combo1_4
    global combo1_1_time,combo1_2_time,combo1_3_time,combo1_4_time
    global bt_label
    global price_label1_1,price_label1_2,price_label1_3,price_label1_4
    bt_label = 4
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    imTK_3 = ImageTk.PhotoImage(img_3.resize((int(img_size/2),int(img_size/2))))
    imTK_4 = ImageTk.PhotoImage(img_4.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size/2,height=img_size/2, bg='blue')
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2, bg='orange')
    div1_3 = tk.Frame(window,width= img_size/2,height=img_size/2, bg='green')
    div1_4 = tk.Frame(window,width= img_size/2,height=img_size/2, bg='black')
    div1_1.grid(column=0, row=0,rowspan=50,columnspan=50, sticky=align_mode)
    div1_2.grid(column=50, row=0,rowspan=50,columnspan=50, sticky=align_mode)
    div1_3.grid(column=0, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    div1_4.grid(column=50, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_3 = tk.Label(div1_3,image=imTK_3)
    image_main_4 = tk.Label(div1_4,image=imTK_4)
    image_main_1.place(x=0,y=0)
    image_main_2.place(x=0,y=0)
    image_main_3.place(x=0,y=0)
    image_main_4.place(x=0,y=0)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=0,y=0)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=0)
    combo1_3 = ttk.Combobox(div1_3,values=coin_list,width=7)
    combo1_3.current(def_coin3)
    combo1_3.place(x=0,y=0)
    combo1_4 = ttk.Combobox(div1_4,values=coin_list,width=7)
    combo1_4.current(def_coin4)
    combo1_4.place(x=0,y=0)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_4.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=80,y=0)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=0)
    combo1_3_time = ttk.Combobox(div1_3, values=time_list,width=5)
    combo1_3_time.current(def_time3)
    combo1_3_time.place(x=80,y=0)
    combo1_4_time = ttk.Combobox(div1_4, values=time_list,width=5)
    combo1_4_time.current(def_time4)
    combo1_4_time.place(x=80,y=0)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_4_time.bind("<<ComboboxSelected>>", choose_token_function)

    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=250,y=0)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=0)
    price_label1_3 = tk.Label(div1_3, text=round(price_dataframe.at['price',combo1_3.get()],2),bg='gray',font=('Arial',10))
    price_label1_3.place(x=250,y=0)
    price_label1_4 = tk.Label(div1_4, text=round(price_dataframe.at['price',combo1_4.get()],2),bg='gray',font=('Arial',10))
    price_label1_4.place(x=250,y=0)
def bt5_windows_seperation(img_1,img_2,img_3,def_coin1,def_time1,def_coin2,def_time2,def_coin3,def_time3):
    global imTK_1 , imTK_2, imTK_3,combo1_1,combo1_2,combo1_3,combo1_1_time,combo1_2_time,combo1_3_time
    global bt_label
    global price_label1_1,price_label1_2,price_label1_3
    bt_label = 5
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    imTK_3 = ImageTk.PhotoImage(img_3.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size/2,height=img_size,bg='blue')
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='orange')
    div1_3 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='green') 
    div1_1.grid(column=0, row=0,rowspan=100,columnspan=50,  sticky=align_mode)
    div1_2.grid(column=50, row=0,rowspan=50,columnspan=50, sticky=align_mode)
    div1_3.grid(column=50, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_3 = tk.Label(div1_3,image=imTK_3)
    image_main_1.place(x=0,y=img_size/4)
    image_main_2.place(x=0,y=0)
    image_main_3.place(x=0,y=0)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=0,y=img_size/4)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=0)
    combo1_3 = ttk.Combobox(div1_3,values=coin_list,width=7)
    combo1_3.current(def_coin3)
    combo1_3.place(x=0,y=0)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3.bind("<<ComboboxSelected>>", choose_token_function)

    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=80,y=img_size/4)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=0)
    combo1_3_time = ttk.Combobox(div1_3, values=time_list,width=5)
    combo1_3_time.current(def_time3)
    combo1_3_time.place(x=80,y=0)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3_time.bind("<<ComboboxSelected>>", choose_token_function)

    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=250,y=img_size/4)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=0)
    price_label1_3 = tk.Label(div1_3, text=round(price_dataframe.at['price',combo1_3.get()],2),bg='gray',font=('Arial',10))
    price_label1_3.place(x=250,y=0)
def bt6_windows_seperation(img_1,img_2,img_3,def_coin1,def_time1,def_coin2,def_time2,def_coin3,def_time3):
    global imTK_1 , imTK_2, imTK_3,combo1_1,combo1_2,combo1_3,combo1_1_time,combo1_2_time,combo1_3_time
    global bt_label
    global price_label1_1,price_label1_2,price_label1_3
    bt_label = 6    
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    imTK_3 = ImageTk.PhotoImage(img_3.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='blue')
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='orange')
    div1_3 = tk.Frame(window,width= img_size,height=img_size/2,bg='green') 
    div1_1.grid(column=0, row=0,rowspan=50,columnspan=50,  sticky=align_mode)
    div1_2.grid(column=50, row=0,rowspan=50,columnspan=50, sticky=align_mode)
    div1_3.grid(column=0, row=50,rowspan=50,columnspan=100, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_3 = tk.Label(div1_3,image=imTK_3)
    image_main_1.place(x=0,y=0)
    image_main_2.place(x=0,y=0)
    image_main_3.place(x=img_size/4,y=0)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=0,y=0)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=0)
    combo1_3 = ttk.Combobox(div1_3,values=coin_list,width=7)
    combo1_3.current(def_coin3)
    combo1_3.place(x=img_size/4,y=0)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3.bind("<<ComboboxSelected>>", choose_token_function)
    
    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=80,y=0)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=0)
    combo1_3_time = ttk.Combobox(div1_3, values=time_list,width=5)
    combo1_3_time.current(def_time3)
    combo1_3_time.place(x=img_size/4+80,y=0)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3_time.bind("<<ComboboxSelected>>", choose_token_function)

    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=250,y=0)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=0)
    price_label1_3 = tk.Label(div1_3, text=round(price_dataframe.at['price',combo1_3.get()],2),bg='gray',font=('Arial',10))
    price_label1_3.place(x=img_size/4+250,y=0)
def bt7_windows_seperation(img_1,img_2,img_3,def_coin1,def_time1,def_coin2,def_time2,def_coin3,def_time3):
    global imTK_1 , imTK_2, imTK_3,combo1_1,combo1_2,combo1_3,combo1_1_time,combo1_2_time,combo1_3_time
    global bt_label
    global price_label1_1,price_label1_2,price_label1_3
    bt_label = 7
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    imTK_3 = ImageTk.PhotoImage(img_3.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size,height=img_size/2,bg='blue')
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='orange')
    div1_3 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='green') 
    div1_1.grid(column=0, row=0,rowspan=50,columnspan=100, sticky=align_mode)
    div1_2.grid(column=0, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    div1_3.grid(column=50, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_3 = tk.Label(div1_3,image=imTK_3)
    image_main_1.place(x=img_size/4,y=0)
    image_main_2.place(x=0,y=0)
    image_main_3.place(x=0,y=0)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=img_size/4,y=0)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=0)
    combo1_3 = ttk.Combobox(div1_3,values=coin_list,width=7)
    combo1_3.current(def_coin3)
    combo1_3.place(x=0,y=0)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=img_size/4+80,y=0)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=0)
    combo1_3_time = ttk.Combobox(div1_3, values=time_list,width=5)
    combo1_3_time.current(def_time3)
    combo1_3_time.place(x=80,y=0)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3_time.bind("<<ComboboxSelected>>", choose_token_function)

    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=img_size/4+250,y=0)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=0)
    price_label1_3 = tk.Label(div1_3, text=round(price_dataframe.at['price',combo1_3.get()],2),bg='gray',font=('Arial',10))
    price_label1_3.place(x=250,y=0)
def bt8_windows_seperation(img_1,img_2,img_3,def_coin1,def_time1,def_coin2,def_time2,def_coin3,def_time3):
    global imTK_1 , imTK_2, imTK_3,combo1_1,combo1_2,combo1_3,combo1_1_time,combo1_2_time,combo1_3_time
    global bt_label
    global price_label1_1,price_label1_2,price_label1_3
    bt_label = 8
    imTK_1 = ImageTk.PhotoImage(img_1.resize((int(img_size/2),int(img_size/2))))
    imTK_2 = ImageTk.PhotoImage(img_2.resize((int(img_size/2),int(img_size/2))))
    imTK_3 = ImageTk.PhotoImage(img_3.resize((int(img_size/2),int(img_size/2))))
    div1_1 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='blue')
    div1_2 = tk.Frame(window,width= img_size/2,height=img_size/2,bg='orange')
    div1_3 = tk.Frame(window,width= img_size/2,height=img_size,bg='green') 
    div1_1.grid(column=0, row=0,rowspan=50,columnspan=50, sticky=align_mode)
    div1_2.grid(column=0, row=50,rowspan=50,columnspan=50, sticky=align_mode)
    div1_3.grid(column=50, row=0,rowspan=100,columnspan=50, sticky=align_mode)
    image_main_1 = tk.Label(div1_1,image=imTK_1)
    image_main_2 = tk.Label(div1_2,image=imTK_2)
    image_main_3 = tk.Label(div1_3,image=imTK_3)
    image_main_1.place(x=0,y=0)
    image_main_2.place(x=0,y=0)
    image_main_3.place(x=0,y=img_size/4)
    #print (img_size)
    combo1_1 = ttk.Combobox(div1_1,values=coin_list,width=7)
    combo1_1.current(def_coin1)
    combo1_1.place(x=0,y=0)
    combo1_2 = ttk.Combobox(div1_2,values=coin_list,width=7)
    combo1_2.current(def_coin2)
    combo1_2.place(x=0,y=0)
    combo1_3 = ttk.Combobox(div1_3,values=coin_list,width=7)
    combo1_3.current(def_coin3)
    combo1_3.place(x=0,y=img_size/4)

    combo1_1.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3.bind("<<ComboboxSelected>>", choose_token_function)

    combo1_1_time = ttk.Combobox(div1_1, values=time_list,width=5)
    combo1_1_time.current(def_time1)
    combo1_1_time.place(x=80,y=0)
    combo1_2_time = ttk.Combobox(div1_2, values=time_list,width=5)
    combo1_2_time.current(def_time2)
    combo1_2_time.place(x=80,y=0)
    combo1_3_time = ttk.Combobox(div1_3, values=time_list,width=5)
    combo1_3_time.current(def_time3)
    combo1_3_time.place(x=80,y=img_size/4)
    combo1_1_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_2_time.bind("<<ComboboxSelected>>", choose_token_function)
    combo1_3_time.bind("<<ComboboxSelected>>", choose_token_function)

    price_label1_1 = tk.Label(div1_1, text=round(price_dataframe.at['price',combo1_1.get()],2),bg='gray',font=('Arial',10))
    price_label1_1.place(x=250,y=0)
    price_label1_2 = tk.Label(div1_2, text=round(price_dataframe.at['price',combo1_2.get()],2),bg='gray',font=('Arial',10))
    price_label1_2.place(x=250,y=0)
    price_label1_3 = tk.Label(div1_3, text=round(price_dataframe.at['price',combo1_3.get()],2),bg='gray',font=('Arial',10))
    price_label1_3.place(x=250,y=img_size/4)
def choose_token_function(event):
    global bt_label
    if bt_label == 1:
        # print("get=",combo1.get(),combo1_time.get())
        idx_coin = combo1.current()
        idx_time = combo1_time.current()
        bt1_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1.get()+combo1_time.get()+'.png'),idx_coin,idx_time)
    if bt_label == 2:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        bt2_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
        Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
        idx_coin1,idx_time1,idx_coin2,idx_time2)
    if bt_label == 3:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        bt3_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2)
    if bt_label == 4:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        print("get1_3=",combo1_3.get())
        print("get1_4=",combo1_4.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_coin3 = combo1_3.current()
        idx_coin4 = combo1_4.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        idx_time3 = combo1_3_time.current()
        idx_time4 = combo1_4_time.current()
        bt4_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_3.get()+combo1_3_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_4.get()+combo1_4_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2,idx_coin3,idx_time3,idx_coin4,idx_time4)
    if bt_label == 5:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        print("get1_3=",combo1_3.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_coin3 = combo1_3.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        idx_time3 = combo1_3_time.current()
        bt5_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_3.get()+combo1_3_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2,idx_coin3,idx_time3)
    if bt_label == 6:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        print("get1_3=",combo1_3.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_coin3 = combo1_3.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        idx_time3 = combo1_3_time.current()
        bt6_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_3.get()+combo1_3_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2,idx_coin3,idx_time3)
    if bt_label == 7:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        print("get1_3=",combo1_3.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_coin3 = combo1_3.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        idx_time3 = combo1_3_time.current()
        bt7_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_3.get()+combo1_3_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2,idx_coin3,idx_time3)
    if bt_label == 8:
        print("get1_1=",combo1_1.get())
        print("get1_2=",combo1_2.get())
        print("get1_3=",combo1_3.get())
        idx_coin1 = combo1_1.current()
        idx_coin2 = combo1_2.current()
        idx_coin3 = combo1_3.current()
        idx_time1 = combo1_1_time.current()
        idx_time2 = combo1_2_time.current()
        idx_time3 = combo1_3_time.current()
        bt8_windows_seperation(Image.open(path+'/'+dataset+ '/'+combo1_1.get()+combo1_1_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_2.get()+combo1_2_time.get()+'.png'),
                               Image.open(path+'/'+dataset+ '/'+combo1_3.get()+combo1_3_time.get()+'.png'),
                               idx_coin1,idx_time1,idx_coin2,idx_time2,idx_coin3,idx_time3)

def gettime():
    global flag_notify , timespan_notify
    global time_set
    global time_const # for time setting (without update immediately)
    #獲取當前時間並轉字符串
    timestr = time.strftime("%H:%M:%S")
    #重設標籤
    label_time.configure(text=timestr)
    #每隔一秒調用函數gettime 獲取時間
    div4.after(1000, gettime)   #after : 特定時間後執行指定函式 #每隔一秒call一次gettime
    # div4.after(10000,message_box_initial)
    current_price() ##抓現價
    
    ## timespan 在 1~5 循環
    timespan_notify %= time_const
    timespan_notify += 1

    #print ("time = ", timespan_notify)
    if flag_notify and timespan_notify == time_const:
        price_notify()  ##行情提醒

    ###### 即時價格更新 ######
    try:        ##fix initial error (mutual try with div seperation)
        if bt_label ==1:
            price_label1.configure(text=round(price_dataframe.at['price',combo1.get()],2))
        if bt_label ==2:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
        if bt_label ==3:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
        if bt_label ==4:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
            price_label1_3.configure(text=round(price_dataframe.at['price',combo1_3.get()],2))
            price_label1_4.configure(text=round(price_dataframe.at['price',combo1_4.get()],2))
        if bt_label ==5:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
            price_label1_3.configure(text=round(price_dataframe.at['price',combo1_3.get()],2))
        if bt_label ==6:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
            price_label1_3.configure(text=round(price_dataframe.at['price',combo1_3.get()],2))
        if bt_label ==7:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
            price_label1_3.configure(text=round(price_dataframe.at['price',combo1_3.get()],2))
        if bt_label ==8:
            price_label1_1.configure(text=round(price_dataframe.at['price',combo1_1.get()],2))
            price_label1_2.configure(text=round(price_dataframe.at['price',combo1_2.get()],2))
            price_label1_3.configure(text=round(price_dataframe.at['price',combo1_3.get()],2))
    except:
        pass
    
    #print("timestr=",timestr.split(":")[0])
    #print("time=",int(time.strftime("%S")))
    update_5m = update_15m = update_30m = update_1h = update_4h = update_1d = 0
    if int(time.strftime("%M"))%5==0 and time.strftime("%S")=='00':     #5m 要求秒數是0
        update_5m = 1
        if int(time.strftime("%M"))%15==0:    #以下層數不要求秒數=0因為可能"已經不是0"了/ 要求M是15的整數倍
            update_15m = 1
            if int(time.strftime("%M"))%30==0:      #要求M是30的整數倍
                update_30m = 1
                if time.strftime("%M") == '00':     #要求M = 0 整點時更新小時級別K線
                    update_1h = 1
                    if int(time.strftime("%H"))%4==0:   #要求H是4的整數倍,以下層數不要求分鐘數=0因為可能已經不是0了!
                        update_4h = 1
                        if time.strftime("%H")=='00':   #要求小時數為0更新日線
                            update_1d = 1
    if update_5m ==1:
        update_figure('5m')
        update_5m = 0
    if update_15m ==1:
        update_figure('15m')
        update_15m = 0
    if update_30m ==1:
        update_figure('30m')
        update_30m = 0
    if update_1h ==1:
        update_figure('1h')
        update_1h = 0
    if update_4h ==1:
        update_figure('4h')
        update_4h = 0
    if update_1d ==1:
        update_figure('1d')
        update_1d = 0


    '''
    ## operating time is too long ##
    if int(time.strftime("%M"))%5==0 and time.strftime("%S")=='00':
        update_figure('5m')
    if int(time.strftime("%M"))%15==0 and time.strftime("%S")=='00':
        update_figure('15m')
    if int(time.strftime("%M"))%30==0 and time.strftime("%S")=='00':
        update_figure('30m')    
    if int(time.strftime("%M"))==0 and time.strftime("%S")=='00':
        update_figure('1h')
    if int(time.strftime("%H"))%4==0 and int(time.strftime("%M"))==0 and time.strftime("%S")=='00':
        update_figure('4h')
    if time.strftime("%H")=='00' and int(time.strftime("%M"))==0 and time.strftime("%S")=='00':
        update_figure('1d')
    ##
    '''

def update_figure(timestamp):
    klinenum = 50
    message_text.configure(text = '"updating {} figure".format(timestamp)')
    # print("updating {} figure".format(timestamp))
    for coin in coin_list:
        kline = GetKline(url, coin, timestamp, klinenum)
        drawklineticker(coin, kline,timestamp,path,dataset)
    choose_token_function(None)
    message_text.configure(text = "{} figure is updated".format(timestamp))
    # print("{} figure is already updated".format(timestamp))

def current_price():
    global price_dataframe
    for i in range (0,len(coin_list)): 
        price_list[i] = GetAvgPrice(url, coin_list[i])
    price_dataframe = pd.DataFrame([price_list])
    price_dataframe.index = ['price']
    price_dataframe.columns = coin_list
    #print("current_price = \n",price_dataframe)
    ####price_dataframe output####
    '''             
        BTCUSDT      ETHUSDT     LTCUSDT   ADAUSDT
price  62877.397558  3794.398617  185.406111  2.120877
    '''
    #print("data=",price_dataframe.at['price','BTCUSDT'])

def message_box_initial():
    time.sleep(5)
    message_text.configure(text= 'Nothing')
    
def Line_notify(key,msg):   
    
    url = ('https://maker.ifttt.com/trigger/Alart/with/'+
          'key/' + key +
          '?value1='+str(msg))
    r = requests.get(url)      
    if r.text[:5] == 'Congr':   #回應的文字若以Congr開頭就表示成功了!
        message_text.configure(text= 'IFTTT connect success!')
        print('成功推送 (' +str(msg)+') 至 Line')
    else:
        message_text.configure(text= 'connect fail!')
    return r.text

# def choose_notify_function(event):
    if choose_num.get() == '1':
        destroy_face()
        global notify_coin_1
        notify_coin_1 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_1.current(0)
        notify_coin_1.grid(column=0, row=1)
    if choose_num.get() == '2':
        global notify_coin_2
        destroy_face()
        notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_2.current(0)
        notify_coin_2.grid(column=0, row=2)
    if choose_num.get() == '3':
        global notify_coin_3
        destroy_face()
        notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_2.current(0)
        notify_coin_2.grid(column=0, row=2)
        notify_coin_3 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_3.current(0)
        notify_coin_3.grid(column=0, row=3)
    if choose_num.get() == '4':
        global notify_coin_4
        destroy_face()
        notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_2.current(0)
        notify_coin_2.grid(column=0, row=2)
        notify_coin_3 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_3.current(0)
        notify_coin_3.grid(column=0, row=3)
        notify_coin_4 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_4.current(0)
        notify_coin_4.grid(column=0, row=4)


# def destroy_face():
    if choose_num.get() == '1':
        try:
            notify_coin_2.destroy()
            try:
                notify_coin_3.destroy()
                try:
                    notify_coin_4.destroy()
                except:
                    pass
            except:
                pass
        except:
            pass
    if choose_num.get() == '2':
        try:
            notify_coin_3.destroy()
            try:
                notify_coin_4.destroy()
            except:
                pass
        except:
            pass
    if choose_num.get() == '3':
        try:
            notify_coin_4.destroy()
        except:
            pass
    if choose_num.get() == '4':
        pass

def plus_notify_coin():
    global coin_num
    if coin_num == 1:
        global notify_coin_2, notify_price_coin_2
        notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_2.current(0)
        notify_coin_2.grid(column=0, row=2, columnspan= 2)
        notify_price_coin_2 = ttk.Entry(div6, width=8)
        notify_price_coin_2.grid(column=2, row=2, columnspan= 2)
        coin_num += 1
    elif coin_num == 2:
        global notify_coin_3, notify_price_coin_3
        notify_coin_3 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_3.current(0)
        notify_coin_3.grid(column=0, row=3, columnspan= 2)
        notify_price_coin_3 = ttk.Entry(div6, width=8)
        notify_price_coin_3.grid(column=2, row=3, columnspan= 2)
        coin_num += 1
    elif coin_num == 3:
        global notify_coin_4, notify_price_coin_4
        notify_coin_4 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_coin_4.current(0)
        notify_coin_4.grid(column=0, row=4, columnspan= 2)
        notify_price_coin_4 = ttk.Entry(div6, width=8)
        notify_price_coin_4.grid(column=2, row=4, columnspan= 2)
        coin_num += 1
    else:
        message_text.configure(text= 'already max!')

def minus_notify_coin():
    global coin_num
    if coin_num == 4:
        notify_coin_4.destroy()
        notify_price_coin_4.destroy()
        default_setting()
        coin_num -=1
        
    elif coin_num == 3:
        notify_coin_3.destroy()
        notify_price_coin_3.destroy()
        default_setting()
        coin_num -=1
        
    elif coin_num == 2:
        notify_coin_2.destroy()
        notify_price_coin_2.destroy()
        default_setting()
        coin_num -=1
        
    else:
        message_text.configure(text= 'already min!')
    pass

def default_setting():
    #global coin_num
    global notify_coin_1, notify_coin_2, notify_coin_3, notify_coin_4, notify_price_coin_1, notify_price_coin_2, notify_price_coin_3, notify_price_coin_4
    if coin_num == 2:
        notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_price_coin_2 = tk.Entry(div6, width=8)
    elif coin_num == 3:
        notify_coin_3 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_price_coin_3 = tk.Entry(div6, width=8)
    elif coin_num == 4:
        notify_coin_4 = ttk.Combobox(div6, values= coin_list,width=8)
        notify_price_coin_4 = tk.Entry(div6, width=8)
    else:
        pass
   
    
    

def price_notify_set():
    global notify_coin, notify_price
    global flag_notify
    global timespan_notify, time_const
    notify_coin = [notify_coin_1.get(), notify_coin_2.get(), notify_coin_3.get(), notify_coin_4.get()]
    notify_price = [notify_price_coin_1.get(), notify_price_coin_2.get(), notify_price_coin_3.get(), notify_price_coin_4.get()]
    msg = '【目標價格提醒】<br>'
    for coin,proc in zip(notify_coin,notify_price):
        try :
            if proc != '':
                msg_temp = "成功設定\"{}\"高於\t{}usdt\t時提醒通知<br>".format(coin,proc)
                msg += msg_temp        
                flag_notify = True
        except Exception as e:
            print(e)
    msg = msg + "時間間隔為\t{}\t秒".format(time_set.get())
    timespan_notify = 0
    time_const = int(time_set.get())
    Line_notify(IFTTT_key.get(),msg)

def price_notify():
    global notify_coin, notify_price
    global timespan_notify
    notify_coin = [notify_coin_1.get(), notify_coin_2.get(), notify_coin_3.get(), notify_coin_4.get()]
    notify_price = [notify_price_coin_1.get(), notify_price_coin_2.get(), notify_price_coin_3.get(), notify_price_coin_4.get()]
    msg = '【目標價格提醒】<br>'

    for coin,proc in zip(notify_coin,notify_price):     # coin/ price definition is same as upon
        try :
            if proc != '':
                if price_dataframe.at['price',coin] > float(proc):
                    msg_temp = "目標\"{}\"高於\t{}usdt\t<br>".format(coin,proc)
                    msg += msg_temp        
                    timespan_notify = 0 # timespan reset
        except Exception as e:
            print(e)
    Line_notify(IFTTT_key.get(),msg)


    # if coin_num == 1:
    #     notify_price_coin_1.get()
    # pass

window = tk.Tk()    #定義一個視窗 叫做window
window.title('window')  #標題
align_mode ='nswe'  #nswe=至中
pad = 1 #向外拓展(pixel)
div_size= 250
img_size = div_size * 3

global flag_notify, timespan_notify
flag_notify = False
timespan_notify = 0

coin_list = ["BTCUSDT","ETHUSDT","LTCUSDT","ADAUSDT"]#define token list used in change img label
time_list = ["5m","15m","30m","1h","4h","1d"]


price_list = [None]*len(coin_list)


#div1 = create_label_image('btcusdt5m.png',0,0,img_size,1,2,pad,align_mode)
div1 = tk.Frame(window,  width=img_size , height=img_size , bg='blue')  #繪圖區
div2 = tk.Frame(window,  bg='orange')    #分割型態區       #abandom width and height
div3 = tk.Frame(window)    #訊息區
div4 = tk.Frame(window,  bg='red')      #TIMER區
div5 = tk.Frame(window, bg = 'blue')    #LINE Notify
div6 = tk.Frame(window, bg = 'green')   #price notify setting

#div4 = tk.Frame(window,  width=div_size , height=div_size , bg='gray')
div1_size=min(div1.winfo_width(),div1.winfo_height())
print('div1_size = ',div1_size)
window.update()
win_size=min(window.winfo_width(),window.winfo_height())
print('win_size = ',win_size)
#div1.grid(column=0, row=0,columnspan=2, rowspan=2)   #rowspan 表示控制元件在Y方向有N個單元格大小跨度
div1.grid(column=0, row=0, padx=pad, pady=pad, rowspan=100, columnspan=100 , sticky=align_mode)
div2.grid(column=100, row=0, padx=pad, pady=pad, rowspan=2, sticky=align_mode)
div3.grid(column=100, row=10, padx=pad, pady=pad, rowspan=20, sticky=align_mode)
div4.grid(column=100, row=2, padx=pad, pady=pad, rowspan=8, sticky=align_mode)
div5.grid(column=100, row=30, padx=pad, pady=pad, rowspan=10, sticky=align_mode)
div6.grid(column=100, row=40, padx=pad, pady=pad, rowspan=20, sticky=align_mode)



#div4.grid(column=5, row=2, padx=pad, pady=pad, rowspan=1, sticky=align_mode)
#定義好UI之後在來處理佈局問題，先來看第一行要注意的地方是如果下層UI要套用權重上層的也一定要套用
#所以如果三個frame要套用的話，最主要的視窗window也需要使用weight分配：

# define_layout(window, cols=4, rows=6)   #←最主要的視窗定義layout
# define_layout([div1])
url  = 'https://api.binance.com/'
url_p = 'https://fapi.binance.com/'
path = os.getcwd()
dataset='img_data'




try:
    os.makedirs(dataset)
except:
    pass
default_coin = 'BTCUSDT'
default_time = '5m'
## default token ###
for num_coin in range (0,len(coin_list)):
    for num_time in range(0, len(time_list)):
        default_klinenum = 50
        kline = GetKline(url, coin_list[num_coin], time_list[num_time], default_klinenum)
        drawklineticker(coin_list[num_coin], kline,time_list[num_time],path,dataset)
        print("drawing {}{}".format(coin_list[num_coin],time_list[num_time]))

im = Image.open(path +'/'+dataset +'/'+default_coin+default_time+'.png')        #default img

#python 讀寫方式r→只讀 , r+→讀寫 不建立, w, w+, a, a+   r+：可讀可寫，若檔案不存在，報錯；w+: 可讀可寫，若檔案不存在，建立 //a：附加寫方式開啟，不可讀；a+: 附加讀寫方式開啟

#im = im.convert("RGB")  #4通道轉3通道
# im.save('btcusdt5m_jpg.jpg')    #3通道轉 jpg and save

# im = Image.open('btcusdt5m_jpg.jpg')    #reload 
bt1_windows_seperation(im,0,0)  #啟動時會先按一下bt1

# Clock
label_time = tk.Label(div4,text='', fg='blue',bg='red',font=('Arial',30))
label_time.pack(expand=1)


##div2(分割)區域
img_bt1 = convert_img_to_tkimg('./GUIPIC/1.jpg',20,20)
img_bt2 = convert_img_to_tkimg('./GUIPIC/2.jpg',20,20)
img_bt3 = convert_img_to_tkimg('./GUIPIC/3.jpg',20,20)
img_bt4 = convert_img_to_tkimg('./GUIPIC/4.jpg',20,20)
img_bt5 = convert_img_to_tkimg('./GUIPIC/5.jpg',20,20)
img_bt6 = convert_img_to_tkimg('./GUIPIC/6.jpg',20,20)
img_bt7 = convert_img_to_tkimg('./GUIPIC/7.jpg',20,20)
img_bt8 = convert_img_to_tkimg('./GUIPIC/8.jpg',20,20)

pad_bt = 20
pad_w = 5
bt1 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt1, bg='orange', fg='white')
bt2 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt2, bg='orange', fg='white')
bt3 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt3, bg='orange', fg='white')
bt4 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt4, bg='orange', fg='white')
bt5 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt5, bg='orange', fg='white')
bt6 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt6, bg='orange', fg='white')
bt7 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt7, bg='orange', fg='white')
bt8 = tk.Button(div2,height=pad_bt,width=pad_bt, image=img_bt8, bg='orange', fg='white')
bt1.grid(column=0, row=0, padx= pad_w, pady= pad_w, sticky=align_mode)
bt2.grid(column=1, row=0, padx= pad_w, pady= pad_w, sticky=align_mode)
bt3.grid(column=2, row=0, padx= pad_w, pady= pad_w, sticky=align_mode)
bt4.grid(column=3, row=0, padx= pad_w, pady= pad_w, sticky=align_mode)
bt5.grid(column=0, row=1, padx= pad_w, pady= pad_w, sticky=align_mode)
bt6.grid(column=1, row=1, padx= pad_w, pady= pad_w, sticky=align_mode)
bt7.grid(column=2, row=1, padx= pad_w, pady= pad_w, sticky=align_mode)
bt8.grid(column=3, row=1, padx= pad_w, pady= pad_w, sticky=align_mode)

#buttom command
bt1['command'] = lambda : bt1_windows_seperation(im,0,0)
bt2['command'] = lambda : bt2_windows_seperation(im,im,0,0,0,0)
bt3['command'] = lambda : bt3_windows_seperation(im,im,0,0,0,0)
bt4['command'] = lambda : bt4_windows_seperation(im,im,im,im,0,0,0,0,0,0,0,0)
bt5['command'] = lambda : bt5_windows_seperation(im,im,im,0,0,0,0,0,0)
bt6['command'] = lambda : bt6_windows_seperation(im,im,im,0,0,0,0,0,0)
bt7['command'] = lambda : bt7_windows_seperation(im,im,im,0,0,0,0,0,0)
bt8['command'] = lambda : bt8_windows_seperation(im,im,im,0,0,0,0,0,0)

######## div3 messagebox ########

message_title = tk.Label(div3, text = 'Message:',height= 1)
message_bg = tk.Label(div3, bg= 'white',width= 50 , height= 50)

message_text = tk.Label(message_bg, text='Nothing',bg = 'white')
message_title.pack(anchor= NW)
message_bg.place(x= 0, y = 20)
message_text.grid(column=0, row=0)

#################################

######## div5 LINE bot ########
global IFTTT_key
LINE_title = tk.Label(div5,text='IFTTT key :')
IFTTT_key = tk.StringVar() # 宣告字串變數
LINE_IFTTT = tk.Entry(div5, width=20, textvariable=IFTTT_key)
check_bt = tk.Button(div5, text='Enter!',width= 5)
#key_te = landString.get()   # 字串變數 不能這樣寫! key_te值不會更新 要直接抓landstring.get()

check_bt['command'] =lambda : Line_notify(IFTTT_key.get(),'連接成功<br>換行測試')  # <br>換行
# check_bt['command'] = lambda : print ("key = ", landString.get())
LINE_title.grid(column=0, row= 0, sticky= tk.W)
LINE_IFTTT.grid(column=0, row= 1)
check_bt.grid(column=0, row= 2)




notify_coin_1 = ttk.Combobox(div6, values= coin_list,width=8)
notify_coin_1.current(0)
notify_coin_1.grid(column=0, row=1, columnspan= 2)
notify_price_coin_1 = tk.Entry(div6, width=8)

global time_set
global time_const
time_const = 5  #default timespan setting
time_set = tk.Entry(div6, width=1)
time_set.insert(0,str(time_const))  #default value
time_set_label = tk.Label(div6,text= "s",bg='green',fg ='white', font=14)
## 預設 以防列表推倒式出錯
notify_coin_2 = ttk.Combobox(div6, values= coin_list,width=8)
notify_coin_3 = ttk.Combobox(div6, values= coin_list,width=8)
notify_coin_4 = ttk.Combobox(div6, values= coin_list,width=8)
notify_price_coin_2 = tk.Entry(div6, width=8)
notify_price_coin_3 = tk.Entry(div6, width=8)
notify_price_coin_4 = tk.Entry(div6, width=8)
#####
notify_price_coin_1.grid(column=2, row=1, columnspan= 2)
plus_bt = tk.Button(div6, text= '+')
minus_bt = tk.Button(div6, text = '-')
plus_bt.grid(column=1,row=0, columnspan= 1)
minus_bt.grid(column=2, row=0, columnspan= 1)
coin_num = 1
plus_bt['command'] = lambda : plus_notify_coin()
minus_bt['command'] = lambda : minus_notify_coin()

notify_bt = tk.Button(div6, text = 'Set', width=5)
notify_bt.grid(column=0, row=5, columnspan= 2, sticky= align_mode)
notify_bt['command'] = lambda : price_notify_set()

time_set.grid(column=2, row=5,sticky = align_mode)
time_set_label.grid(column=3, row=5, sticky = align_mode)
# bt_1g = tk.Button(div3, text='Button 1', bg='green', fg='white')
# bt_2g = tk.Button(div3, text='Button 2', bg='green', fg='white')
# bt_3g = tk.Button(div3, text='Button 3', bg='green', fg='white')
# bt_4g = tk.Button(div3, text='Button 4', bg='green', fg='white')
# bt_1g.grid(column=0, row=0, sticky=align_mode)
# bt_2g.grid(column=0, row=1, sticky=align_mode)
# bt_3g.grid(column=0, row=2, sticky=align_mode)
# bt_4g.grid(column=0, row=3, sticky=align_mode)
#bt_1g['command'] = lambda : get_size(window, image_main, im)  #another command is →partials
#define_layout(window, cols=2, rows=2) 
# define_layout(div1)
# define_layout(div2, cols=4, rows=2)       #有放layout就會把div塞滿


#define_layout(div3, rows=4)


#window.geometry('600x800')  #設定像素大小    沒有給的話視窗會自動調整

#create_label('GUI test')
#create_button('Button')
#create_label_image('btcusdt5m.png')

gettime()
window.mainloop()
# %%
