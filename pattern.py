from tkinter import *
from tkinter import ttk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, extract_images, display_icon, resize_img, display_images
from functions import *
import numpy as np
from tkinter.filedialog import askopenfilename, askopenfile
import os
import numpy as np
from numpy import reshape
from matplotlib import pyplot as plt
import cv2
import camogen
import matplotlib.pyplot as plt
from camogen.generate import generate
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans
from tkmacosx import Button as button
import rcnn_detection
import filter
import overlap
import overlap
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
# image varuables
masked_array = None
filtered_array = None
def content_generator():
    parameters = {'width': int(pattern_setting["width"].get("1.0", 'end-1c')),
                  'height': int(pattern_setting["height"].get("1.0", 'end-1c')),
                  'polygon_size': int(pattern_setting["polygon_size"].get("1.0", 'end-1c')),
                  'color_bleed': int(pattern_setting["color_bleed"].get("1.0", 'end-1c')),
                  'max_depth': int(pattern_setting["max_depth"].get("1.0", 'end-1c')),
                  'colors': hexadecimal,
                  'spots': {'amount': int(spot_setting["amount"].get("1.0", 'end-1c')),
                            'radius': {'min': int(spot_setting["radius_min"].get("1.0", 'end-1c')),
                                       'max': int(spot_setting["radius_max"].get("1.0", 'end-1c'))},
                            'sampling_variation': int(spot_setting["sampling_variation"].get("1.0", 'end-1c'))},
                  'pixelize': {'percentage': float(pixelization["percentage"].get("1.0", 'end-1c')),
                               'sampling_variation': int(pixelization["pixelization_variation"].get("1.0", 'end-1c')),
                               'density': {'x': int(pixelization["density_x"].get("1.0", 'end-1c')),
                                           'y': int(pixelization["density_y"].get("1.0", 'end-1c'))}}}

    num_pattern = 5  # Number of patterns generated at a time
    camo_pattern.clear()
    for i in range(num_pattern):
        camo_pattern.append(generate(parameters))

    print("camo pattern", camo_pattern[0])
    display_images(camo_pattern[0])  # this function displays images
    overlapped = overlap.overlap_camo(filtered_array, camo_pattern[0])
    display_images(overlapped,3,10,1, 1)
    tmp = "Image 1 of " + str(num_pattern)
    what_img_label = Label(root, text="Image 1 of ", font=("shanti", 15, 'bold'), bg="#126e82")
    what_img_label.grid(row=3, column=6)

    display_icon("arrow_l.png", row=3, column=5, stick=E)
    display_icon("arrow_r.png", row=3, column=7, stick=W)


def set_default_setting(default_pattern):
    default = default_pattern.get()
    tmp = ['100', '100', '50', '1', '8', '200000', '1', '10', '5', '1', '20', '50', '50']
    if default == "Pixal1":
        tmp = ['100', '100', '50', '1', '8', '200000', '1', '10', '5', '1', '20', '50', '50']
    elif default == "Blots1":
        tmp = ['700', '700', '200', '6', '15', '20000', '7', '14', '10', '0', '0', '0', '0']
    elif default == "Vodka1":
        tmp = ['700', '700', '200', '0', '15', '3000', '30', '40', '10', '0.75', '10', '60', '100']
    elif default == "Maple1":
        tmp = ['700', '700', '150', '3', '15', '500', '20', '30', '20', '1', '20', '70', '50']

    # min_length = min(len(pattern_setting), min(len(spot_setting), len(pixelization)))
    for p1, p2, p3 in zip(pattern_setting.keys(), spot_setting.keys(), pixelization.keys()):
        pattern_setting[p1].delete('1.0', END)
        spot_setting[p2].delete('1.0', END)
        pixelization[p3].delete('1.0', END)
        pattern_setting[p1].grid_forget()
        spot_setting[p2].grid_forget()
        pixelization[p3].grid_forget()
    pattern_setting["max_depth"].delete('1.0', END)
    pattern_setting["max_depth"].grid_forget()

    pattern_setting["width"].insert(END, tmp[0])
    pattern_setting["height"].insert(END, tmp[1])
    pattern_setting["polygon_size"].insert(END, tmp[2])
    pattern_setting["color_bleed"].insert(END, tmp[3])
    pattern_setting["max_depth"].insert(END, tmp[4])

    spot_setting["amount"].insert(END, tmp[5])
    spot_setting["radius_min"].insert(END, tmp[6])
    spot_setting["radius_max"].insert(END, tmp[7])
    spot_setting["sampling_variation"].insert(END, tmp[8])

    pixelization["percentage"].insert(END, tmp[9])
    pixelization["pixelization_variation"].insert(END, tmp[10])
    pixelization["density_x"].insert(END, tmp[11])
    pixelization["density_y"].insert(END, tmp[12])

    pattern_setting["width"].grid(column=1, row=4, padx=0, pady=1, sticky=W)
    pattern_setting["height"].grid(column=1, row=5, padx=0, pady=1, sticky=W)
    pattern_setting["polygon_size"].grid(column=1, row=6, padx=0, pady=1, sticky=W)
    pattern_setting["color_bleed"].grid(column=1, row=7, padx=0, pady=1, sticky=W)
    pattern_setting["max_depth"].grid(column=1, row=8, padx=0, pady=1, sticky=W)
    # Spots text
    spot_setting["amount"].grid(column=3, row=5, padx=0, pady=1, sticky=W)
    spot_setting["radius_min"].grid(column=3, row=6, padx=0, pady=1, sticky=W)
    spot_setting["radius_max"].grid(	column=3, row=7, padx=0, pady=1, sticky=W)
    spot_setting["sampling_variation"].grid(column=3, row=8, padx=0, pady=1, sticky=W)
    # Pixelization text
    pixelization["percentage"].grid(			column=5, row=5, padx=0, pady=1, sticky=W)
    pixelization["pixelization_variation"].grid(column=5, row=6, padx=0, pady=1, sticky=W)
    pixelization["density_x"].grid(			    column=5, row=7, padx=0, pady=1, sticky=W)
    pixelization["density_y"].grid(			    column=5, row=8, padx=0, pady=1, sticky=W)


def generate_pattern():
    generate_content = Frame(root, width=1200, height=50, bg="#126e82")
    generate_content.grid(columnspan=8, rowspan=1, row=3)

    cofig_label = Label(root, text="Set Pattern Configurations", font=("shant" ,20, 'bold'), bg="#126e82")
    cofig_label.grid(row=3, column=1, columnspan=2)

    default_pattern = StringVar(root)
    default_pattern.set("Choose Default Config")
    question_menu = OptionMenu(root, default_pattern, *["Pixal1", "Blots1", "Vodka1", "Maple1"],
                               command=lambda x=None: set_default_setting(default_pattern))
    question_menu.config(bg="#126e82")  # Set background color to green
    # Set this to what you want, I'm assuming "green"...
    question_menu["menu"].config(bg="#126e82")
    question_menu.grid(row=3, column=4)

    # Generators Frame
    main_content = Frame(root, width=1200, height=350, bg="#132c33")
    main_content.grid(columnspan=8, rowspan=7, row=4)

    # Configuration Inputs
    label_width = Label(root, text="Width:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                        bg="#132c33", fg="white")
    pattern_setting["width"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_height = Label(root, text="Height:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                         bg="#132c33", fg="white")
    pattern_setting["height"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_polygon_size = Label(root, text="Polygon Size:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1,
                               pady=1, bg="#132c33", fg="white")
    pattern_setting["polygon_size"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_color_bleed = Label(root, text="Color Bleed:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1,
                              pady=1, bg="#132c33", fg="white")
    pattern_setting["color_bleed"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_max_depth = Label(root, text="Max Depth:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                            bg="#132c33", fg="white")
    pattern_setting["max_depth"] = Text(root, height=1, width=15, padx=1, pady=1)
    # Spot and Pixelization

    label_Spot = Label(root, text="Spot Settings", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                       bg="#132c33", fg="white")
    label_spots_amount = Label(root, text="Amount:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                               bg="#132c33", fg="white")
    spot_setting["amount"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_spots_radius_min = Label(root, text="Radius Min:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1,
                                   pady=1, bg="#132c33", fg="white")
    spot_setting["radius_min"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_spots_radius_max = Label(root, text="Radius Max:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1,
                                   pady=1, bg="#132c33", fg="white")
    spot_setting["radius_max"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_spots_sampling_variation = Label(root, text="Variation:", font=("shanti", 15, 'bold'), height=1, width=10,
                                           padx=1, pady=1, bg="#132c33", fg="white")
    spot_setting["sampling_variation"] = Text(root, height=1, width=15, padx=1, pady=1)

    # Pixelization
    label_pixelization = Label(root, text="Pixelization Settings", font=("shanti", 15, 'bold'), height=1, width=20,
                               padx=1, pady=1, bg="#132c33", fg="white")
    label_percentage = Label(root, text="percentage:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                             bg="#132c33", fg="white")
    pixelization["percentage"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_pixelization_variation = Label(root, text="Variation:", font=("shanti", 15, 'bold'), height=1, width=10,
                                         padx=1, pady=1, bg="#132c33", fg="white")
    pixelization["pixelization_variation"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_density_x = Label(root, text="Density X:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                            bg="#132c33", fg="white")
    pixelization["density_x"] = Text(root, height=1, width=15, padx=1, pady=1)

    label_density_y = Label(root, text="Density Y:", font=("shanti", 15, 'bold'), height=1, width=10, padx=1, pady=1,
                            bg="#132c33", fg="white")
    pixelization["density_y"] = Text(root, height=1, width=15, padx=1, pady=1)

    # Set Default values for parameters generation
    set_default_setting(default_pattern)
    # Display setting
    label_width.grid(column=0, row=4, padx=10, pady=1, sticky=E)
    label_height.grid(column=0, row=5, padx=10, pady=1, sticky=E)
    label_polygon_size.grid(column=0, row=6, padx=10, pady=1, sticky=E)
    label_color_bleed.grid(column=0, row=7, padx=10, pady=1, sticky=E)
    label_max_depth.grid(column=0, row=8, padx=10, pady=1, sticky=E)

    pattern_setting["width"].grid(column=1, row=4, padx=0, pady=1, sticky=W)
    pattern_setting["height"].grid(	column=1, row=5, padx=0, pady=1, sticky=W)
    pattern_setting["polygon_size"].grid(column=1, row=6, padx=0, pady=1, sticky=W)
    pattern_setting["color_bleed"].grid( column=1, row=7, padx=0, pady=1, sticky=W)
    pattern_setting["max_depth"].grid(	column=1, row=8, padx=0, pady=1, sticky=W)

    # Spots
    label_Spot.grid( 	  columnspan=2, column=2, row=4, padx=0, pady=1)
    label_spots_amount.grid(			column=2, row=5, padx=5, pady=1, sticky=E)
    label_spots_radius_min.grid(		column=2, row=6, padx=5, pady=1, sticky=E)
    label_spots_radius_max.grid(		column=2, row=7, padx=5, pady=1, sticky=E)
    label_spots_sampling_variation.grid(column=2, row=8, padx=5, pady=1, sticky=E)

    # Spots text
    spot_setting["amount"].grid(			column=3, row=5, padx=0, pady=1, sticky=W)
    spot_setting["radius_min"].grid(		column=3, row=6, padx=0, pady=1, sticky=W)
    spot_setting["radius_max"].grid(		column=3, row=7, padx=0, pady=1, sticky=W)
    spot_setting["sampling_variation"].grid(column=3, row=8, padx=0, pady=1, sticky=W)

    # Pixelization
    label_pixelization.grid(columnspan=2, column=4, row=4, padx=0, pady=1)
    label_percentage.grid(			  	  column=4, row=5, padx=5, pady=1, sticky=E)
    label_pixelization_variation.grid(	  column=4, row=6, padx=5, pady=1, sticky=E)
    label_density_x.grid(				  column=4, row=7, padx=5, pady=1, sticky=E)
    label_density_y.grid(				  column=4, row=8, padx=5, pady=1, sticky=E)
    # Pixelization text
    pixelization["percentage"].grid(			column=5, row=5, padx=0, pady=1, sticky=W)
    pixelization["pixelization_variation"].grid(column=5, row=6, padx=0, pady=1, sticky=W)
    pixelization["density_x"].grid(			    column=5, row=7, padx=0, pady=1, sticky=W)
    pixelization["density_y"].grid(			    column=5, row=8, padx=0, pady=1, sticky=W)

    # Submit button
    submit_label = button(root, text="Generate", height=35, width=100 ,command=content_generator,
                          font=("Raleway", 12, "bold"), bg="black", fg="white")
    submit_label.grid(column=3, row=9, sticky="W")


def remove_all():
    if messagebox.askokcancel("Restart", "Do you want to Restart?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)


def display_color(color, row, column, pnt="\n00%"):
    btn_text = str(color + pnt)
    button_label = button(root, text=btn_text, height=100, width=100, command=lambda: delete_color(button_label, color),
                          font=("Raleway", 15), bg=color, fg="white")
    button_label.grid(column=column, row=row)


def delete_color(button_label, to_delete):
    button_label.grid_forget()
    if to_delete in hexadecimal:
        hexadecimal.remove(to_delete)

    if to_delete in choosen_color:
        choosen_color.remove(to_delete)


# def popup_bonus():
#     win = Toplevel()
#     win.wm_title("Error while choosing colours")

#     l = Label(win, text="Cannot load more than 7 colours, please delete by clicking the colour buttons")
#     l.grid(row=200, column=200)

#     b = ttk.Button(win, text="Got it!", command=win.destroy)
#     b.grid(row=201, column=200)

def choose():
    if len(hexadecimal) < 7:
        add_color = colorchooser.askcolor()[1]
        hexadecimal.append(add_color)
        choosen_color.append(add_color)
        idx = 0
        for color in hexadecimal:
            if color in color_score.keys():
                display_color(color, 2, idx, color_score[color])
            else:
                display_color(color, 2, idx)
            idx += 1
    else:
        messagebox.showinfo("Error while choosing colours",
                            "Cannot load more than 7 colours, please delete first by clicking the colour buttons")


def extract_color(image):
    if image.mode != "RGB":
        image = image.convert("RGB")
    numpy_image = np.array(image)
    # print(numpy_image.shape)
    width, height = numpy_image.shape[0:2]
    pixel = numpy_image.reshape((height * width, 3))

    km = MiniBatchKMeans(n_clusters=int(dominant_color.get()))
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

    global score
    score = np.unique(km.labels_, return_counts=True)[1]
    idx = 0
    for color in hexadecimal:
        color_score[color] = "\n " + str(np.round((score[idx] * 100) / len(km.labels_), 2)) + "%"
        display_color(color, 2, idx, color_score[color])
        idx += 1

    for color in choosen_color:
        display_color(color, 2, idx)
        idx += 1
    browse_text.set("Browse")


root = Tk()
root.title("Camoflauge Generator")
root.geometry('+%d+%d' % (0, 10))  # place GUI at x=350, y=10

# header area - logo & browse button
header = Frame(root, width=1200, height=175, bg="white")
header.grid(columnspan=8, rowspan=2, row=0)

color_content = Frame(root, width=1200, height=150, bg="#51c4d3")
color_content.grid(columnspan=8, rowspan=1, row=2)


# main content area - text and image extraction
# main_content = Frame(root, width=800, height=250, bg="#20bebe")
# main_content.grid(columnspan=3, rowspan=2, row=4)

def open_file():
    browse_text.set("loading...")
    # file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
    filename = askopenfilename()
    img = None
    if filename:
        img = Image.open(filename)  # .resize( Image.NEAREST(225, 225))) # the one-liner I used in my app
        # img = ImageTk.PhotoImage(img)
        # image_label = Label(root, image=img)
        # image_label.image = img # this feels redundant but the image didn't show up without it in my app
    if img:
        global masked_array
        masked_array, results = rcnn_detection.detect(np.array(img))
        masked = Image.fromarray(masked_array.astype(np.uint8))
        display_images(masked, 1, 10, 1, 1)
        global filtered_array
        filtered_array,cropped = filter.remove_single_object(np.array(img),results,1)
        print(filtered_array)
        filtered = Image.fromarray(filtered_array.astype(np.uint8))
        display_images(filtered,2,10, 1, 1)
        extract_color(filtered)




# Display Logo
display_logo('chameleon.png', row=0, column=0, columnspan=2)
# instructions
instructions = Label(root, text="Select an Image", font=("Raleway", 15, 'bold'), bg="white")
instructions.grid(column=7, row=0, columnspan=1, sticky=SE, padx=50, pady=5)

# browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda: open_file(),
                    font=("Raleway", 12, 'bold'), highlightbackground="#20bebe",
                    bg="#20bebe", fg="black", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=7, row=1, columnspan=1, sticky=NE, padx=50)

choose_color = Button(root, text="Pick a color", command=choose,
                      font=("Raleway", 12), highlightbackground="#20bebe",
                      bg="#20bebe", fg="black", height=2, width=15)
choose_color.grid(column=5, row=1, sticky=NE)

dominant_color = StringVar(root)
dominant_color.set(5)
question_menu = OptionMenu(root, dominant_color, *options_list)
question_menu.grid(column=6, row=0, sticky=SE)

extraction_method = StringVar(root)
extraction_method.set("Terrain")
question_menu = OptionMenu(root, extraction_method, *["Terrain", "Terrain with object"])
question_menu.grid(column=6, row=1, sticky=NE)
restart_app = Button(root, text="Restart App", command=remove_all,
                     font=("Raleway", 12), highlightbackground="#20bebe",
                     bg="#20bebe", fg="black", height=2, width=15)
restart_app.grid(column=4, row=1, sticky=NE)

generate_btn = Button(root, text="Generate Pattern", command=generate_pattern,
                      font=("Raleway", 12), highlightbackground="#20bebe",
                      bg="#20bebe", fg="black", height=2, width=15)
generate_btn.grid(column=7, row=2)

root.mainloop()
