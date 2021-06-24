import tkinter as tk
from tkinter import colorchooser, messagebox
import os
from tkinter import colorchooser, messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import MiniBatchKMeans
from tkmacosx import Button as button

import filter
import overlap
import rcnn_detection
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
# image_array variables
img = None
masked_array = None
filtered_array = None
cropped_array = None
results = None
# temporary implementation for pattern
# program states
from enum import Enum


class STATES(Enum):
    load_image = 1
    view_pattern = 2
    efficiency_test = 3


current_state = STATES.load_image
tmp = ['1000', '1000', '150', '3', '15', '500', '20', '30', '20', '100', '20', '50', '50']
# functions
from enum import Enum


def camo_generator():
    parameters = {'width': int(tmp[0]), 'height': int(tmp[1]),
                  'polygon_size': int(tmp[2]), 'color_bleed': int(tmp[3]),
                  'max_depth': int(tmp[4]), 'colors': hexadecimal,
                  'spots': {'amount': int(tmp[5]),
                            'radius': {'min': int(tmp[6]), 'max': int(tmp[7])},
                            'sampling_variation': int(tmp[8])
                            },
                  'pixelize': {'percentage': float(tmp[9]) / 100,
                               'sampling_variation': int(tmp[10]),
                               'density': {'x': int(tmp[11]), 'y': int(tmp[12])}
                               }
                  }
    camo_pattern = generate(parameters)
    camo_pattern = camo_pattern.resize((500, 500))
    camo_image = ImageTk.PhotoImage(camo_pattern, master=image_view)
    pattern_label.configure(image=camo_image)
    pattern_label.image = camo_image
    print("camo pattern", camo_pattern)

    if len(filtered_array) > 0 and len(cropped_array) > 0:
        overlapped = overlap.overlap_camo(filtered_array, cropped_array, camo_pattern)
        overlapped.thumbnail((500, 250))
        overlap_image = ImageTk.PhotoImage(overlapped, master=image_view)
        overlay_image_label.configure(image=overlap_image)
        overlay_image_label.image = overlap_image


def extract_color(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    numpy_image = np.array(image)
    # print(numpy_image.shape)
    width, height = numpy_image.shape[0:2]
    pixel = numpy_image.reshape((height * width, 3))

    km = MiniBatchKMeans(n_clusters=int(5))
    km.fit(pixel)
    minibatch_centers = np.array(km.cluster_centers_, dtype='uint8')
    avg = [0, 0, 0]
    for x in minibatch_centers:
        if not (x[0] < 10 and x[1] < 10 and x[2] < 10):
            avg += (x / len(minibatch_centers) - 1)
    print(avg)
    for x in range(len(minibatch_centers)):
        if minibatch_centers[x][0] < 10 and minibatch_centers[x][1] < 10 and minibatch_centers[x][2] < 10:
            minibatch_centers[x] = avg
    hexadecimal.clear()
    for array in minibatch_centers:
        hexadecimal.append('#%02x%02x%02x' % (array[0], array[1], array[2]))
    idx = 0
    global score
    score = np.unique(km.labels_, return_counts=True)[1]
    for color in hexadecimal:
        color_score[color] = "\n " + str(np.round((score[idx] * 100) / len(km.labels_), 2)) + "%"
        idx += 1


def restart():
    if messagebox.askokcancel("Restart", "Do you want to Restart?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)


def enter_load_image():
    setup_params()
    top_right_button.place(x=(800 - 200) * scale_x, y=0, width=200 * scale_x, height=50 * scale_y)
    top_left_button.configure(text="Restart App")
    bottom_left_button.configure(text="Proceed")


def enter_view_pattern():
    setup_params()
    if img:
        camo_generator()
    top_right_button.place_forget()
    top_left_button.configure(text="go back")
    bottom_left_button.configure(text="efficiency test")


def enter_efficiency_test():
    setup_params()
    bottom_left_button.configure(text="save_pattern")


def setup_params():
    width_label = Label(param_bar, text="width", bg="white")
    pattern_setting["width"] = Text(param_bar)
    height_label = Label(param_bar, text="height", bg="white")
    pattern_setting["height"] = Text(param_bar)
    polygon_size_label = Label(param_bar, text="polygon_size", bg="white")
    pattern_setting["polygon_size"] = Text(param_bar)
    color_bleed_label = Label(param_bar, text="color_bleed", bg="white")
    pattern_setting["color_bleed"] = Text(param_bar)
    max_depth_label = Label(param_bar, text="max_depth", bg="white")
    pattern_setting["max_depth"] = Text(param_bar)
    spots_label = Label(param_bar, text="spots", bg="white")
    spots_amount_label = Label(param_bar, text="spots size", bg="white")
    spot_setting["amount"] = Text(param_bar)
    spots_radius_label = Label(param_bar, text="radius", bg="white")
    spots_radius_label_min = Label(param_bar, text="min", bg="white")
    spot_setting["min"] = Text(param_bar)
    spots_radius_label_max = Label(param_bar, text="max", bg="white")
    spot_setting["max"] = Text(param_bar)
    spots_sampling_variation_label = Label(param_bar, text="sampling_variation", bg="white")
    spot_setting["sampling_variation"] = Text(param_bar)
    pixelize_label = Label(param_bar, text="pixelize", bg="white")
    pixelize_percentage_label = Label(param_bar, text="percentage", bg="white")
    pixelization["percentage"] = Text(param_bar)
    pixelize_sampling_variation_label = Label(param_bar, text="sampling_variation", bg="white")
    pixelization["sampling_variation"] = Text(param_bar)
    pixelize_density_label = Label(param_bar, text="density", bg="white")
    pixelize_density_x_label = Label(param_bar, text="x", bg="white")
    pixelization["x"] = Text(param_bar)
    pixelize_density_y_label = Label(param_bar, text="y", bg="white")
    pixelization["y"] = Text(param_bar)
    build_button = Button(param_bar, text="Rebuild", bg="white", command=lambda: camo_generator())
    if current_state == STATES.view_pattern:
        _height = 25
        width_label.place(x=0, y=_height * 0, width=100 * scale_x, height=_height)
        height_label.place(x=100 * scale_x, y=_height * 0, width=100 * scale_x, height=_height)
        pattern_setting["width"].place(x=0, y=_height * 1, width=100 * scale_x, height=_height)
        pattern_setting["height"].place(x=100 * scale_x, y=_height * 1, width=100 * scale_x, height=_height)
        polygon_size_label.place(x=0, y=_height * 2, width=100 * scale_x, height=_height)
        color_bleed_label.place(x=100 * scale_x, y=_height * 2, width=100* scale_x, height=_height)
        pattern_setting["polygon_size"].place(x=0, y=_height * 3, width=100 * scale_x, height=_height)
        pattern_setting["color_bleed"].place(x=100 * scale_x, y=_height * 3, width=100 * scale_x, height=_height)
        max_depth_label.place(x=50* scale_x, y=_height * 4, width=100 * scale_x, height=_height)
        pattern_setting["max_depth"].place(x=50* scale_x, y=_height * 5, width=100 * scale_x, height=_height)
        spots_label.place(x=50* scale_x, y=_height * 6, width=100 * scale_x, height=_height)
        spots_amount_label.place(x=0, y=_height * 7, width=100 * scale_x, height=_height)
        spots_sampling_variation_label.place(x=100 * scale_x, y=_height * 7, width=100 * scale_x, height=_height)
        spot_setting["amount"].place(x=0, y=_height * 8, width=100 * scale_x, height=_height)
        spot_setting["sampling_variation"].place(x=100 * scale_x, y=_height * 8, width=100 * scale_x, height=_height)
        spots_radius_label.place(x=50* scale_x, y=_height * 9, width=100 * scale_x, height=_height)
        spots_radius_label_min.place(x=0, y=_height * 10, width=100 * scale_x, height=_height)
        spots_radius_label_max.place(x=100 * scale_x, y=_height * 10, width=100 * scale_x, height=_height)
        spot_setting["min"].place(x=0, y=_height * 11, width=100 * scale_x, height=_height)
        spot_setting["max"].place(x=100 * scale_x, y=_height * 11, width=100 * scale_x, height=_height)
        pixelize_label.place(x=50* scale_x, y=_height * 12, width=100 * scale_x, height=_height)
        pixelize_percentage_label.place(x=0, y=_height * 13, width=100 * scale_x, height=_height)
        pixelize_sampling_variation_label.place(x=100 * scale_x, y=_height * 13, width=100 * scale_x, height=_height)
        pixelization["percentage"].place(x=0, y=_height * 14, width=100 * scale_x, height=_height)
        pixelization["sampling_variation"].place(x=100 * scale_x, y=_height * 14, width=100 * scale_x, height=_height)
        pixelize_density_label.place(x=50* scale_x, y=_height * 15, width=100 * scale_x, height=_height)
        pixelize_density_x_label.place(x=0, y=_height * 16, width=100 * scale_x, height=_height)
        pixelize_density_y_label.place(x=100 * scale_x, y=_height * 16, width=100 * scale_x, height=_height)
        pixelization["x"].place(x=0, y=_height * 17, width=100 * scale_x, height=_height)
        pixelization["y"].place(x=100 * scale_x, y=_height * 17, width=100 * scale_x, height=_height)
        build_button.place(x=50*scale_x,y =_height * 19, width=100 * scale_x,height=_height)
    else:
        width_label.place_forget()
        height_label.place_forget()
        pattern_setting["width"].place_forget()
        pattern_setting["height"].place_forget()
        max_depth_label.place_forget()
        pattern_setting["max_depth"].place_forget()
        spots_label.place_forget()
        spots_amount_label.place_forget()
        spots_sampling_variation_label.place_forget()
        spot_setting["amount"].place_forget()
        spot_setting["sampling_variation"].place_forget()
        spots_radius_label.place_forget()
        spots_radius_label_min.place_forget()
        spots_radius_label_max.place_forget()
        spot_setting["min"].place_forget()
        spot_setting["max"].place_forget()
        pixelize_label.place_forget()
        pixelize_percentage_label.place_forget()
        pixelize_sampling_variation_label.place_forget()
        pixelization["percentage"].place_forget()
        pixelization["sampling_variation"].place_forget()
        pixelize_density_label.place_forget()
        pixelize_density_x_label.place_forget()
        pixelize_density_y_label.place_forget()
        pixelization["x"].place_forget()
        pixelization["y"].place_forget()
        build_button.place_forget()
# commands
def top_left_button_command():  # restart_app or go back
    global current_state
    if current_state == STATES.load_image:
        # restart app
        restart()
        pass
    elif current_state == STATES.view_pattern:
        current_state = STATES.load_image
        enter_load_image()
        pass
    elif current_state == STATES.efficiency_test:
        current_state = STATES.view_pattern
        enter_view_pattern()
        pass


def bottom_left_button_command():  # proceed or save pattern/image
    global current_state
    if current_state == STATES.load_image:
        current_state = STATES.view_pattern
        enter_view_pattern()
        pass
    elif current_state == STATES.view_pattern:
        current_state = STATES.efficiency_test
        enter_efficiency_test()
        pass
    elif current_state == STATES.efficiency_test:
        # save image
        pass


def top_right_button_command():  # load image
    filename = askopenfilename()
    global img
    if filename:
        img = Image.open(filename)
    if img:
        img.thumbnail((500, 250))
        load_image = ImageTk.PhotoImage(img, master=image_view)
        loaded_image_label.configure(image=load_image)
        loaded_image_label.image = load_image
        global masked_array
        global results
        masked_array, results = rcnn_detection.detect(np.array(img))
        detected_objects = ""
        for ids in results['class_ids']:
            detected_objects += "|" + rcnn_detection.class_names[ids] + "|"
        detected_label.configure(text=detected_objects)
        detected_label.text = detected_objects
        global filtered_array
        global cropped_array
        if results["rois"].shape[0]:
            filtered_array, cropped_array = filter.remove_single_object(np.array(img), results, 0)
            filtered = Image.fromarray(filtered_array.astype(np.uint8))
            extract_color(filtered)
        else:
            filtered_array = None
            extract_color(img)


# root, UI elements , everything calculated from top left
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
top_left_button = Button(header, bd=0, text="Restart App", command=top_left_button_command)
top_left_button.place(x=0, y=0, width=200 * scale_x, height=50 * scale_y)
top_right_button = Button(header, bd=0, text="Load image", command=top_right_button_command)
top_right_button.place(x=(800 - 200) * scale_x, y=0, width=200 * scale_x, height=50 * scale_y)
bottom_left_button = Button(footer, bd=0, text="Proceed", command=bottom_left_button_command)
bottom_left_button.place(x=0, y=0, width=200 * scale_x, height=50 * scale_y)
pattern_label = Label(image_view, bg="white")
pattern_label.place(x=0, y=0, width=500, height=500)
loaded_image_label = Label(image_view, bg="black")
loaded_image_label.place(x=500, y=0, width=500, height=250)
overlay_image_label = Label(image_view, bg="yellow")
overlay_image_label.place(x=500, y=250, width=500, height=250)
detected_label = Label(footer, text="Detected objects", bg="white")
detected_label.place(relx=(3 / 8.0), y=10 * scale_y, width=400 * scale_x, height=30 * scale_y)
root.mainloop()
