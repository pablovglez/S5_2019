#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 17:36:42 2019

@author: efisio
"""

import tkinter
from tkinter import scrolledtext

import threading
import time
import tkinter

top = tkinter.Tk()
top.title("RLTS Angle of Arrival")
top.geometry('650x400')
txt = scrolledtext.ScrolledText(top,width=40,height=10)
txt.grid(column=0,row=0)

def loop1_10():
    for i in range(1, 11):
        time.sleep(0.5)
        print(i)
        txt.insert(tkinter.END,i)
        txt.insert(tkinter.END,"\n")

threading.Thread(target=loop1_10).start()

#txt.insert(tkinter.INSERT,'Test to write here....')
txt.insert(tkinter.END,"Hola")
txt.insert(tkinter.END,"\n")
top.mainloop()