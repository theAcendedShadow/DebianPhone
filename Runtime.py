import tkinter as tk
import customtkinter as ctk
import os 
import json
import bezel
#bezel library ~ liases with bezels from config.json
from PIL import Image, ImageDraw, ImageTk
from PIL import *

#config
with open("config.json", 'r') as file:
    config = file.read()
    config = json.loads(config)
version = config['os']['os']
screenGeom = config['display']['screensize']
appgrid = config['display']['appgrid']
wallpaper = config['display']['wallpaper']
topbezel = config['display']['topbezel']
bottombezel = config['display']['bottombezel']
font = (config["display"]["font"], config["display"]["fsize"], config["display"]["ftype"])
Debug = True
if Debug:
    screenGeom = [512, 640]

class Window:
    #establishes the base class of a tkinter window
    def __init__(self):
        
        #creates the main window of the variable
        self.root  = ctk.CTk()
        self.children = []
        #creates an unfilled list for child nodes
        
        # This removes the grey title bar capsule completely!
        self.root.overrideredirect(True)

        self.root.bind("<Escape>", lambda e: self.root.destroy())
        if type(self) != Window:
            self.customSetup()
            #if the user is calling a fork of the Window class an extra function called customsetup
            #adds more function to __init__()

    
    def start(self):
        #initialises the window
        self.root.mainloop()

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
        if type(self) == MioLauncher:
            self.xcount += 1
            x = self.xcount
            if self.xcount == appgrid[0]:
                self.ycount += 1
                y = self.ycount
                self.xcount = 0
                x = self.xcount
            else:
                y = self.ycount
            self.childpos.append([x, y])
            print(self.xcount)



class MioLauncher(Window):
    #a type designed to launch applications and serve as the DE for the Phone
    def customSetup(self):
        #config
        intScreenGeom = str(screenGeom[0]) + "x" + str(screenGeom[1])
        self.root.geometry(intScreenGeom)
        self.root.title(f"MioS Launcher {version}")
        #trancparency second layer
        self.root.resizable(False, False)
        #non resizable
        self.frame = ctk.CTkCanvas(self.root, bg=self.root["bg"], bd=0, highlightthickness=0)
        yPos = 0 + topbezel
        usableheight = screenGeom[1] - topbezel - bottombezel
        self.frame.place(x=0, y=yPos, width=screenGeom[0], height=usableheight)
        self.apply_background()
        self.apply_bezels()
        #self.background.lift()
        self.childpos = []
        self.xcount = -1
        self.ycount = 0 


    def apply_background(self):
        with open("config.json", 'r') as file:
            config = file.read()
            config = json.loads(config)
            wallpaper = config['display']['wallpaper']
            file.close()
        newScreenHeight = screenGeom[1]
        if config['display']['topbezelcontent'] != []:
            newScreenHeight -= topbezel
        if config['display']['bottombezelcontent'] != []:
            newScreenHeight -= bottombezel
        
        self.background_image = Image.open(wallpaper).convert("RGBA").resize((screenGeom[0], newScreenHeight), Image.Resampling.LANCZOS)
        self.background_image = ImageTk.PhotoImage(self.background_image)
        #creates an image based on the config screensize and file
        print(screenGeom)
        #self.background = ctk.CTkLabel(self.root, image=self.background_image, text="")
        #self.background.place(relwidth=1,relheight=1)
        self.frame.create_image(0, 0, image=self.background_image, anchor="nw")
        #displays image

    def apply_bezels(self):
        if config['display']['topbezelcontent'] != []:
            self.top_bezel = Bezel(self.root, yCentering="top", xCentering="left", xLen=screenGeom[0], yLen=topbezel, content=config['display']['topbezelcontent'])
        if config['display']['bottombezelcontent'] != []:
            self.bottom_bezel = Bezel(self.root, yCentering="bottom", xCentering="left", xLen=screenGeom[0], yLen=bottombezel, content=config['display']['bottombezelcontent'])


class Button:
    def __init__(self, image, window, clickable=False, text=None, application=None, function=None, buttonsize=None, radius=90):
        if buttonsize == None:
            if appgrid[0] <= appgrid[1] :
                buttonsize = ((round(screenGeom[0]/ appgrid[0]), (round(screenGeom[0]/appgrid[0]))))
            else:
                buttonsize = ((round(screenGeom[0]/ appgrid[1]), (round(screenGeom[0]/appgrid[1]))))
        window.addChild(self)
        self.size, self.root, self.radius = buttonsize, window.frame, radius
        self.icon = self.roundICN(image)
        #self.image = ctk.CTkImage(dark_image=self.icon, light_image=self.icon, size=(self.size))
        self.config = {"clickable":clickable, "text":text, "application":application, "function":function}
        #self.ui = ctk.CTkLabel(self.root, image=self.image, text="", bg_color="transparent")
        self.developedIcon = ImageTk.PhotoImage(self.icon)
        self.getPos()
        self.canvas = self.root.create_image(self.x, self.y, image=self.developedIcon, anchor="nw")
        
        

    def roundICN(self, image):
        #open and force trancparency and size
        self.size = (round(self.size[0] / 1.5), round(self.size[1] / 1.5))
        img = Image.open(image).convert("RGBA").resize(self.size, Image.Resampling.LANCZOS)

            
            #antialiasing
        scale = 4
        maskw, maskh = self.size[0] * scale, self.size[1] * scale
        maskradius = self.radius * scale

        mask = Image.new("L", (maskw, maskh), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, maskw, maskh), radius=maskradius, fill=255)
        mask = mask.resize(self.size, Image.Resampling.LANCZOS)
        img.putalpha(mask)
        return img

    def getPos(self):
        pos = self.parent.children.index(self)
        gridslotx = screenGeom[0] / appgrid[0]
        yheight = screenGeom[1] - topbezel - bottombezel
        gridsloty = yheight / appgrid[1]
        cellwidthoffset = (gridslotx - self.size[0]) / 2
        cellheightoffset = (gridsloty - self.size[1]) / 2
        self.x = (self.parent.childpos[pos][0]) * round(screenGeom[0] / appgrid[0]) + cellwidthoffset
        self.y = (self.parent.childpos[pos][1]) * round(screenGeom[1] / appgrid[1]) + cellheightoffset
        print(self.x, self.y)

class Bezel:
    def __init__(self, root, yCentering="top", xCentering="mid", xLen=None, yLen=None, devType=ctk.CTkLabel, content = []):
        if type(yCentering) == str:
            centeringTypes = [["top", 0], ["bottom", screenGeom[1] - yLen - 2]]
            for types in centeringTypes:
                if types[0] == yCentering:
                    yPos = types[1]
            if yPos is None:
                yPos = 0
                print(f"error in {self} unknown y centering")
        else:
            yPos = yCentering
        if type(xCentering) == str:
            centeringTypes = [["mid", round(screenGeom[0] / 2)], ["right", screenGeom[0]], ["left", 0]]
            for types in centeringTypes:
                if types[0] == xCentering:
                    xPos = types[1]
            if xPos is None:
                xPos = 0
                print(f"error in {self} unknown x centering")
        else:
            xPos = xCentering

        if yLen is None:
            yLen = 30
        if xLen is None:
            xLen = screenGeom[0]

        self.xPos, self.yPos = xPos, yPos  
        self.content = content
        self.widgets = []

        if devType == ctk.CTkLabel:
            self.main = ctk.CTkLabel(root, width=xLen, height=yLen, text="", fg_color="#242424", anchor="center", padx=0, pady=0)
        if devType == tk.Label:
            self.main = tk.Label(root, width=xLen, height=yLen, bg="#242424", anchor="center", padx=0, pady=0)
        if devType == ctk.CTkButton:
            self.main = ctk.CTkButton(root, width=xLen, height=yLen, anchor="center", padx=0, pady=0)
        if devType == tk.Button:
            self.main = tk.Button(root, width=xLen, height=yLen, anchor="center", padx=0, pady=0)
        self.main.place(x=xPos, y=yPos)
        self.main.lift() # Pulls the background strip forward

        try:
            content_division = screenGeom[0] / len(content)
            content_division = round(content_division)
            for index, cont in enumerate(content):
                if hasattr(bezel, cont):
                    xPos_child = content_division * index
                    cmnd = getattr(bezel, cont)
                    
                    # Target self.main instead of root, and lock the vertical alignment offset to 0
                    attribute = cmnd(self.main, width=content_division, height=yLen, x=xPos_child, y=0)
                    self.widgets.append(attribute)
                    if attribute:
                        attribute.lift()
                
        except ZeroDivisionError:
            self.main.configure(text="No content detected")
            print(f"no bezel content provided for {self}, try setting bezel height to zero")



    
launcher = MioLauncher()
apps = []
for i in range(appgrid[0] * appgrid[1]):
    if (i + 1) % 2 == 0: 
        apps.append(Button(image="Pictures/tstIcn.png", window=launcher))
    else:
        apps.append(Button(image="Pictures/testIcn3.png", window=launcher))

print(launcher.children)
launcher.start()