#This is a library that holds all of the commands utilised by config.json bezels
import json, PIL, time
import tkinter as tk
import tkinter.font as tkfont
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw

def rtc(window, width, height, x=0, y=0):
    with open("config.json", 'r') as f:
        config = f.read()
        config = json.loads(config)
        font = (config["display"]["font"], config["display"]["fsize"], config["display"]["ftype"])

    rtc_label = ctk.CTkLabel(window, width=width, height=height, text="04:20", font=font, bg_color="transparent", anchor="center")
    rtc_label.place(x=x, y=y)
    update_rtc(rtc_label, width)
    return rtc_label

def update_rtc(rtc_label, width):
    #fetch current font
    font = rtc_label.cget("font")

    #convert it for tkinter measurment tools
    font_tk = tkfont.Font(font=font)

    #generate potential time varients
    extendedRealTime = time.strftime("%H:%M")
    abridgedRealTime = time.strftime("%H:%M")

    #find length of full time
    time_pix_len = font_tk.measure(extendedRealTime)

    #if the width of text is larger than the allocated width use abridged width
    if time_pix_len < width:
        realTime = extendedRealTime
    else:
        realTime = abridgedRealTime
    rtc_label.configure(text=realTime)
    rtc_label.after(1000, lambda: update_rtc(rtc_label, width))


def os(window, width, height, x=0, y=0):
    with open ("config.json", "r") as f:
        config = f.read()
        config = json.loads(config)
        font = (config["display"]["font"], config["display"]["fsize"], config["display"]["ftype"])


    osText = config["os"]["os"]

    os_label = ctk.CTkLabel(window, width=width, height=height, text=osText, font=font, bg_color="transparent", anchor="center")

    #fetch current font
    font = os_label.cget("font")

    #convert it for tkinter measurment tools
    font_tk = tkfont.Font(family=font[0], size=font[1], weight=font[2] if len(font) > 2 else "normal")

    #if the width of text is larger than the allocated width use abridged width
    os_pix_length = font_tk.measure(osText)
    if os_pix_length < width:
        osText = config["os"]["osshort"]

    os_label = ctk.CTkLabel(window, width=width, height=height, text=osText, font=font, bg_color="transparent", anchor="center", padx=0, pady=0)
    os_label.place(x=x, y=y)
    return os_label

