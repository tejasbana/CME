import tkinter as tk
from tkinter import colorchooser, messagebox
import os
from tkinter import colorchooser, messagebox
from tkinter.filedialog import askopenfilename

import numpy as np
from sklearn.cluster import MiniBatchKMeans
from tkmacosx import Button as button

import filter
import overlap
# import rcnn_detection
from camogen.generate import generate
from functions import *

# page_contents=[]
# all_images=[]
# img_idx = [0]
# displayed_img = []
options_list = [1, 2, 3, 4, 5, 6, 7]
hexadecimal = []
choosen_color = []
color_score = {}
# Generators setting variables
pattern_setting = {}
spot_setting = {}
pixelization = {}
# Pattern Generator
selected_pattern = 0
camo_pattern = []
# image_array variables
masked_array = None
filtered_array = None
cropped_array = None
# commands
from enum import Enum
def enter_load_image():
    top_left_button.configure(text= "Restart App")
    bottom_left_button.configure(text="Proceed")
def enter_view_pattern():
    top_left_button.configure(text = "go back")
    bottom_left_button.configure(text ="efficiency test")
def enter_efficiency_test():
    bottom_left_button.configure(text = "save_pattern")
class STATES(Enum):
    load_image = 1
    view_pattern = 2
    efficiency_test = 3
current_state = STATES.load_image
def top_left_button_command():# restart_app or go back
    global current_state
    if current_state == STATES.load_image:
        #restart app
        pass
    elif current_state == STATES.view_pattern:
        enter_load_image()
        current_state = STATES.load_image
        pass
    elif current_state == STATES.efficiency_test:
        enter_view_pattern()
        current_state = STATES.view_pattern
        pass
def bottom_left_button_command():# proceed or save pattern/image
    global current_state
    if current_state == STATES.load_image:
        enter_view_pattern()
        current_state = STATES.view_pattern
        pass
    elif current_state == STATES.view_pattern:
        enter_efficiency_test()
        current_state = STATES.efficiency_test
        pass
    elif current_state == STATES.efficiency_test:
        # save image
        pass



# root, UI elements
root = Tk()
scale_x = 1.5
scale_y = 1
root.title("Camoflauge Generator")
root.geometry('%dx%d+%d+%d' % (800 * scale_x, 600 * scale_y, 0, 10))  # place GUI at x=0, y=10
root.resizable(False, False)
header = Frame(root, width=800 * scale_x, height=50 * scale_y, bg="green")
header.place(x=0, y=0)
footer = Frame(root, width=800 * scale_x, height=50 * scale_y, bg="black")
footer.place(x=0, y=550 * scale_y)
param_bar = Frame(root, width=200 * scale_x, height=500 * scale_y, bg="brown")
param_bar.place(x=0, y=50 * scale_y)
image_view = Frame(root, width=600 * scale_x, height=500 * scale_y, bg="grey")
image_view.place(x=200 * scale_x, y=50 * scale_y)
top_left_button = Button(header,bd= 0,text="Restart App",command=top_left_button_command)
top_left_button.place(x=0,y=0,width=200*scale_x,height=50*scale_y)
bottom_left_button = Button(footer,bd= 0,text="Proceed",command=bottom_left_button_command)
bottom_left_button.place(x=0,y=0,width=200*scale_x,height=50*scale_y)
root.mainloop()

