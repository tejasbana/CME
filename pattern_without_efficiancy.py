import tkinter as tk
from tkinter import *
import os
from tkinter import messagebox, filedialog, colorchooser
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import MiniBatchKMeans
import filter
import overlap
import math
import rcnn_detection
from camogen.generate import generate

hexadecimal = []
choosen_color = []
max_color_limit = 7
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


current_state = STATES.load_image
tmp = ['1000', '1000', '150', '3', '15', '500', '20', '30', '20', '100', '20', '50', '50']
# functions
from enum import Enum


def camo_generator():
    parameters = {'width': int(pattern_setting["width"].get("1.0", 'end-1c')),
                  'height': int(pattern_setting["height"].get("1.0", 'end-1c')),
                  'polygon_size': int(pattern_setting["polygon_size"].get("1.0", 'end-1c')),
                  'color_bleed': int(pattern_setting["color_bleed"].get("1.0", 'end-1c')),
                  'max_depth': int(pattern_setting["max_depth"].get("1.0", 'end-1c')),
                  'colors': hexadecimal,
                  'spots': {'amount': int(spot_setting["amount"].get("1.0", 'end-1c')),
                            'radius': {'min': int(spot_setting["min"].get("1.0", 'end-1c')),
                                       'max': int(spot_setting["max"].get("1.0", 'end-1c'))},
                            'sampling_variation': int(spot_setting["sampling_variation"].get("1.0", 'end-1c'))
                            },
                  'pixelize': {'percentage': float(pixelization["percentage"].get("1.0", 'end-1c')) / 100,
                               'sampling_variation': int(pixelization["sampling_variation"].get("1.0", 'end-1c')),
                               'density': {'x': int(pixelization["x"].get("1.0", 'end-1c')),
                                           'y': int(pixelization["y"].get("1.0", 'end-1c'))}
                               }
                  }
    camo_pattern = generate(parameters)
    camo_pattern = camo_pattern.resize((500, 500))
    camo_image = ImageTk.PhotoImage(camo_pattern, master=image_view)
    pattern_label.configure(image=camo_image)
    pattern_label.image = camo_image
    print("camo pattern", camo_pattern)
    if filtered_array is not None and cropped_array is not None:
        if len(filtered_array) > 0 and len(cropped_array) > 0:
            overlapped = overlap.overlap_camo(filtered_array, cropped_array, camo_pattern)
            overlapped.thumbnail((500, 250))
            overlap_image = ImageTk.PhotoImage(overlapped, master=image_view)
            overlay_image_label.configure(image=overlap_image)
            overlay_image_label.image = overlap_image


def set_default_setting():
    print("def set", tmp)
    # clean up tmp
    for p1, p2, p3 in zip(pattern_setting.keys(), spot_setting.keys(), pixelization.keys()):
        pattern_setting[p1].delete('1.0', END)
        spot_setting[p2].delete('1.0', END)
        pixelization[p3].delete('1.0', END)
        pattern_setting[p1].grid_forget()
        spot_setting[p2].grid_forget()
        pixelization[p3].grid_forget()
    pattern_setting["max_depth"].delete('1.0', END)
    # insert values
    pattern_setting["width"].insert(END, tmp[0])
    pattern_setting["height"].insert(END, tmp[1])
    pattern_setting["polygon_size"].insert(END, tmp[2])
    pattern_setting["color_bleed"].insert(END, tmp[3])
    pattern_setting["max_depth"].insert(END, tmp[4])

    spot_setting["amount"].insert(END, tmp[5])
    spot_setting["min"].insert(END, tmp[6])
    spot_setting["max"].insert(END, tmp[7])
    spot_setting["sampling_variation"].insert(END, tmp[8])

    pixelization["percentage"].insert(END, tmp[9])
    pixelization["sampling_variation"].insert(END, tmp[10])
    pixelization["x"].insert(END, tmp[11])
    pixelization["y"].insert(END, tmp[12])


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
    btn_text = ""
    for i in choosen_color:
        i.destroy()
    choosen_color.clear()
    for i in range(0,len(hexadecimal)):
        if hexadecimal[i] in color_score.keys():
            btn_text = str(hexadecimal[i] + color_score[hexadecimal[i]])
        button_label = Label(param_bar, bg=hexadecimal[i] , text=btn_text, height=50, width=50 , command=lambda: delete_color(button_label,color))
        x_place = 50 * (i % 4)
        choosen_color.append(button_label)
        y_place = 50 * (math.floor((i+1) / 4.1))
        print(i," ",x_place, " ", y_place)
        button_label.place(x=x_place * scale_x, y=y_place, width=50 * scale_x, height=50 * scale_y)


def cache_params():
    if all(len(pattern_setting[key].get("1.0", 'end-1c')) != 0 for key in pattern_setting.keys()):
        tmp[0] = pattern_setting["width"].get("1.0", 'end-1c')
        tmp[1] = pattern_setting["height"].get("1.0", 'end-1c')
        tmp[2] = pattern_setting["polygon_size"].get("1.0", 'end-1c')
        tmp[3] = pattern_setting["color_bleed"].get("1.0", 'end-1c')
        tmp[4] = pattern_setting["max_depth"].get("1.0", 'end-1c')
    if all(len(spot_setting[key].get("1.0", 'end-1c')) != 0 for key in spot_setting.keys()):
        tmp[5] = spot_setting["amount"].get("1.0", 'end-1c')
        tmp[6] = spot_setting["min"].get("1.0", 'end-1c')
        tmp[7] = spot_setting["max"].get("1.0", 'end-1c')
        tmp[8] = spot_setting["sampling_variation"].get("1.0", 'end-1c')
    if all(len(pixelization[key].get("1.0", 'end-1c')) != 0 for key in pixelization.keys()):
        tmp[9] = pixelization["percentage"].get("1.0", 'end-1c')
        tmp[10] = pixelization["sampling_variation"].get("1.0", 'end-1c')
        tmp[11] = pixelization["x"].get("1.0", 'end-1c')
        tmp[12] = pixelization["y"].get("1.0", 'end-1c')
    print("cache params", tmp)

'''
def restart():
    if messagebox.askokcancel("Restart", "Do you want to Restart?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)'''


def enter_load_image():
    setup_color()
    setup_params()
    top_right_button.place(x=(800 - 200) * scale_x, y=0, width=200 * scale_x, height=50 * scale_y)
    top_left_button.configure(text="Add Color")
    bottom_left_button.configure(text="Proceed")


def enter_view_pattern():
    setup_color()
    setup_params()
    overlay_image_label.config(image='')
    if img or len(hexadecimal) > 0:
        set_default_setting()
        camo_generator()
    top_right_button.place_forget()
    top_left_button.configure(text="go back")
    bottom_left_button.configure(text="save_pattern")


def exit_view_pattern():
    cache_params()


def savefile():
    save_img = ImageTk.getimage(pattern_label.image)
    print("save image is ", save_img)
    file = filedialog.asksaveasfile(title='Save image', mode='w', defaultextension=".png")
    if file is None:
        return
    abs_path = os.path.abspath(file.name)
    save_img.save(abs_path, "PNG")


def setup_params():
    if current_state == STATES.view_pattern:
        _height = 25
        width_label.place(x=0, y=_height * 0, width=100 * scale_x, height=_height)
        height_label.place(x=100 * scale_x, y=_height * 0, width=100 * scale_x, height=_height)
        pattern_setting["width"].place(x=0, y=_height * 1, width=100 * scale_x, height=_height)
        pattern_setting["height"].place(x=100 * scale_x, y=_height * 1, width=100 * scale_x, height=_height)
        polygon_size_label.place(x=0, y=_height * 2, width=100 * scale_x, height=_height)
        color_bleed_label.place(x=100 * scale_x, y=_height * 2, width=100 * scale_x, height=_height)
        pattern_setting["polygon_size"].place(x=0, y=_height * 3, width=100 * scale_x, height=_height)
        pattern_setting["color_bleed"].place(x=100 * scale_x, y=_height * 3, width=100 * scale_x, height=_height)
        max_depth_label.place(x=50 * scale_x, y=_height * 4, width=100 * scale_x, height=_height)
        pattern_setting["max_depth"].place(x=50 * scale_x, y=_height * 5, width=100 * scale_x, height=_height)
        spots_label.place(x=50 * scale_x, y=_height * 6, width=100 * scale_x, height=_height)
        spots_amount_label.place(x=0, y=_height * 7, width=100 * scale_x, height=_height)
        spots_sampling_variation_label.place(x=100 * scale_x, y=_height * 7, width=100 * scale_x, height=_height)
        spot_setting["amount"].place(x=0, y=_height * 8, width=100 * scale_x, height=_height)
        spot_setting["sampling_variation"].place(x=100 * scale_x, y=_height * 8, width=100 * scale_x, height=_height)
        spots_radius_label.place(x=50 * scale_x, y=_height * 9, width=100 * scale_x, height=_height)
        spots_radius_label_min.place(x=0, y=_height * 10, width=100 * scale_x, height=_height)
        spots_radius_label_max.place(x=100 * scale_x, y=_height * 10, width=100 * scale_x, height=_height)
        spot_setting["min"].place(x=0, y=_height * 11, width=100 * scale_x, height=_height)
        spot_setting["max"].place(x=100 * scale_x, y=_height * 11, width=100 * scale_x, height=_height)
        pixelize_label.place(x=50 * scale_x, y=_height * 12, width=100 * scale_x, height=_height)
        pixelize_percentage_label.place(x=0, y=_height * 13, width=100 * scale_x, height=_height)
        pixelize_sampling_variation_label.place(x=100 * scale_x, y=_height * 13, width=100 * scale_x, height=_height)
        pixelization["percentage"].place(x=0, y=_height * 14, width=100 * scale_x, height=_height)
        pixelization["sampling_variation"].place(x=100 * scale_x, y=_height * 14, width=100 * scale_x, height=_height)
        pixelize_density_label.place(x=50 * scale_x, y=_height * 15, width=100 * scale_x, height=_height)
        pixelize_density_x_label.place(x=0, y=_height * 16, width=100 * scale_x, height=_height)
        pixelize_density_y_label.place(x=100 * scale_x, y=_height * 16, width=100 * scale_x, height=_height)
        pixelization["x"].place(x=0, y=_height * 17, width=100 * scale_x, height=_height)
        pixelization["y"].place(x=100 * scale_x, y=_height * 17, width=100 * scale_x, height=_height)
        build_button.place(x=50 * scale_x, y=_height * 19, width=100 * scale_x, height=_height)
    else:
        print("forget")
        print(width_label)
        width_label.place_forget()
        height_label.place_forget()
        polygon_size_label.place_forget()
        color_bleed_label.place_forget()
        pattern_setting["width"].place_forget()
        pattern_setting["height"].place_forget()
        pattern_setting["polygon_size"].place_forget()
        pattern_setting["color_bleed"].place_forget()
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


def add_color():
    if len(hexadecimal) < max_color_limit:
        color = colorchooser.askcolor()[1]
        hexadecimal.append(color)
        print("add color")
        btn_text = ""
        if color is None:
            return
        for color in hexadecimal:
            if color in color_score.keys():
                btn_text = str(color + color_score[color])
            else:
                btn_text = str(color)
        button_label = Button(param_bar, bg=color, text=btn_text, height=50, width=50,command=lambda: delete_color(button_label,color),highlightbackground=color)
        x_place = 50 * (len(choosen_color) % 4)
        choosen_color.append(button_label)
        y_place = 50 * (math.floor(len(choosen_color) / 4.1))
        print(x_place, " ", y_place)
        button_label.place(x=x_place * scale_x, y=y_place, width=50 * scale_x, height=50 * scale_y)


def delete_color(button_label, to_delete):
    button_label.destroy()
    if to_delete in hexadecimal:
        hexadecimal.remove(to_delete)
    if button_label in choosen_color:
        choosen_color.remove(button_label)
    setup_color()


def setup_color():
    if current_state == STATES.load_image:
        for i in range(0, len(choosen_color)):
            x_place = 50 * (i % 4)
            y_place = 50 * (math.floor((i+1) / 4.1))
            choosen_color[i].place(x=x_place * scale_x, y=y_place * scale_y, width=50 * scale_x, height=50 * scale_y)
    else:
        for i in choosen_color:
            i.place_forget()


# commands
def top_left_button_command():  # restart_app or go back
    global current_state
    if current_state == STATES.load_image:
        add_color()
        pass
    elif current_state == STATES.view_pattern:
        exit_view_pattern()
        current_state = STATES.load_image
        enter_load_image()
        pass


def bottom_left_button_command():  # proceed or save pattern/image
    global current_state
    if current_state == STATES.load_image:
        current_state = STATES.view_pattern
        enter_view_pattern()
        pass
    elif current_state == STATES.view_pattern:
        savefile()
        # save image
        pass


def top_right_button_command():  # load image
    filename = askopenfilename()
    global img
    if filename:
        img = Image.open(filename)
    else:
        loaded_image_label.configure(image="")
        img = None
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
            background, images = filter.remove_multi_object(np.array(img), results)
            extract_color(Image.fromarray(background.astype(np.uint8)))
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
# Fixed UI
header = Frame(root, width=800 * scale_x, height=50 * scale_y, bg="#2B411C")
header.place(x=0, y=0)
footer = Frame(root, width=800 * scale_x, height=50 * scale_y, bg="#2B411C")
footer.place(x=0, y=550 * scale_y)
param_bar = Frame(root, width=200 * scale_x, height=500 * scale_y, bg="#5B7742")
param_bar.place(x=0, y=50 * scale_y)
image_view = Frame(root, width=600 * scale_x, height=500 * scale_y, bg="#A4AA88")
image_view.place(x=200 * scale_x, y=50 * scale_y)
top_left_button = Button(header, bg="#4C5D34", text="Add Color", command=top_left_button_command,highlightbackground='#4C5D34')
top_left_button.place(x=0, y=0, width=200 * scale_x, height=50 * scale_y)
top_right_button = Button(header, bg="#4C5D34", text="Load image", command=top_right_button_command,highlightbackground='#4C5D34')
top_right_button.place(x=(800 - 200) * scale_x, y=0, width=200 * scale_x, height=50 * scale_y)
bottom_left_button = Button(footer, bg="#4C5D34", text="Proceed", command=bottom_left_button_command,highlightbackground='#4C5D34')
bottom_left_button.place(x=0, y=0, width=200 * scale_x, height=50 * scale_y)
pattern_label = Label(image_view, bg="#A4AA88")
pattern_label.place(x=0, y=0, width=500, height=500)
loaded_image_label = Label(image_view, bg="#A4AA88")
loaded_image_label.place(x=500, y=0, width=500, height=250)
overlay_image_label = Label(image_view, bg="#A4AA88")
overlay_image_label.place(x=500, y=250, width=500, height=250)
detected_label = Label(footer, text="Detected objects", bg="#4C5D34")
detected_label.place(relx=(3 / 8.0), y=10 * scale_y, width=400 * scale_x, height=30 * scale_y)
# changing UI
# visualize pattern params UI
width_label = Label(param_bar, text="width", bg="#A4AA88")
pattern_setting["width"] = Text(param_bar, bg="#5B7742")
height_label = Label(param_bar, text="height", bg="#A4AA88")
pattern_setting["height"] = Text(param_bar, bg="#5B7742")
polygon_size_label = Label(param_bar, text="polygon_size", bg="#A4AA88")
pattern_setting["polygon_size"] = Text(param_bar, bg="#5B7742")
color_bleed_label = Label(param_bar, text="color_bleed", bg="#A4AA88")
pattern_setting["color_bleed"] = Text(param_bar, bg="#5B7742")
max_depth_label = Label(param_bar, text="max_depth", bg="#A4AA88")
pattern_setting["max_depth"] = Text(param_bar, bg="#5B7742")
spots_label = Label(param_bar, text="spots", bg="#A4AA88")
spots_amount_label = Label(param_bar, text="spots size", bg="#A4AA88")
spot_setting["amount"] = Text(param_bar, bg="#5B7742")
spots_radius_label = Label(param_bar, text="radius", bg="#A4AA88")
spots_radius_label_min = Label(param_bar, text="min", bg="#A4AA88")
spot_setting["min"] = Text(param_bar, bg="#5B7742")
spots_radius_label_max = Label(param_bar, text="max", bg="#A4AA88")
spot_setting["max"] = Text(param_bar, bg="#5B7742")
spots_sampling_variation_label = Label(param_bar, text="sampling_variation", bg="#A4AA88")
spot_setting["sampling_variation"] = Text(param_bar, bg="#5B7742")
pixelize_label = Label(param_bar, text="pixelize", bg="#A4AA88")
pixelize_percentage_label = Label(param_bar, text="percentage", bg="#A4AA88")
pixelization["percentage"] = Text(param_bar, bg="#5B7742")
pixelize_sampling_variation_label = Label(param_bar, text="sampling_variation", bg="#A4AA88")
pixelization["sampling_variation"] = Text(param_bar, bg="#5B7742")
pixelize_density_label = Label(param_bar, text="density", bg="#A4AA88")
pixelize_density_x_label = Label(param_bar, text="x", bg="#A4AA88")
pixelization["x"] = Text(param_bar, bg="#5B7742")
pixelize_density_y_label = Label(param_bar, text="y", bg="#A4AA88")
pixelization["y"] = Text(param_bar, bg="#5B7742")
build_button = Button(param_bar, text="Rebuild", bg="#A4AA88", command=lambda: camo_generator())
root.mainloop()
