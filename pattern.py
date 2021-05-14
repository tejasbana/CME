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


page_contents=[]
all_images=[]
img_idx = [0]
displayed_img = []
options_list = [1,2,3,4,5,6,7]
hexadecimal = []
choosen_color = []
color_score = {}
# Generators setting variables
pattern_setting = {}
spot_setting = {}
pixelization = {}

def content_generator():
	parameters = {'width': int( pattern_setting["width"].get("1.0",'end-1c') ), 'height': int( pattern_setting["height"].get("1.0",'end-1c') ), 'polygon_size': int( pattern_setting["polygon_size"].get("1.0",'end-1c') ), 'color_bleed': int( pattern_setting["color_bleed"].get("1.0",'end-1c') ), 'max_depth': int( pattern_setting["max_depth"].get("1.0",'end-1c') ),
				  'colors': hexadecimal,
				  'spots': {'amount': int( spot_setting["amount"].get("1.0",'end-1c') ), 'radius': {'min': int(spot_setting["radius_min"].get("1.0",'end-1c') ), 'max': int( spot_setting["radius_max"].get("1.0",'end-1c') ) }, 'sampling_variation': int(spot_setting["sampling_variation"].get("1.0",'end-1c') ) },
				  'pixelize': {'percentage': int( pixelization["percentage"].get("1.0",'end-1c') ), 'sampling_variation': int( pixelization["pixelization_variation"].get("1.0",'end-1c') ), 'density': {'x': int( pixelization["density_x"].get("1.0",'end-1c') ), 'y': int( pixelization["density_y"].get("1.0",'end-1c')) }}}
	camo_pattern = generate(parameters)
	display_images(camo_pattern)

def set_default_setting():
	pattern_setting["width"].insert(END, '100')
	pattern_setting["height"].insert(END, '100')
	pattern_setting["polygon_size"].insert(END, '50')
	pattern_setting["color_bleed"].insert(END, '1')
	pattern_setting["max_depth"].insert(END, '8')

	spot_setting["amount"].insert(END, '200000')
	spot_setting["radius_min"].insert(END, '1')
	spot_setting["radius_max"].insert(END, '10')
	spot_setting["sampling_variation"].insert(END, '5')

	pixelization["percentage"].insert(END, '1')
	pixelization["pixelization_variation"].insert(END, '20')
	pixelization["density_x"].insert(END, '50')
	pixelization["density_y"].insert(END, '50')

def generate_pattern():
	generate_content = Frame(root, width=1200, height=50, bg="#126e82")
	generate_content.grid(columnspan=8, rowspan=1, row=3)

	cofig_label = Label(root, text="Set Pattern Configurations", font=("shanti",20,'bold'), bg="#126e82")
	cofig_label.grid(row=3, column=2, columnspan=2)

	what_img_label = Label(root, text="Image 1 of 5", font=("shanti",15,'bold'), bg="#126e82")
	what_img_label.grid(row=3, column=6)

	display_icon("arrow_l.png", row=3, column=5, stick=E)
	display_icon("arrow_r.png", row=3, column=7, stick=W)
	# Generators Frame
	main_content = Frame(root, width=1200, height=350, bg="#132c33")
	main_content.grid(columnspan=8, rowspan=7, row=4)

	# Configuration Inputs
	label_width = Label(root, text="Width:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pattern_setting["width"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_height = Label(root, text="Height:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pattern_setting["height"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_polygon_size = Label(root, text="Polygon Size:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pattern_setting["polygon_size"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_color_bleed = Label(root, text="Color Bleed:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pattern_setting["color_bleed"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_max_depth = Label(root, text="Max Depth:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pattern_setting["max_depth"] = Text(root, height=1, width=15, padx=1, pady=1)
	# Spot and Pixelization

	label_Spot = Label(root, text="Spot Settings", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	label_spots_amount = Label(root, text="Amount:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	spot_setting["amount"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_spots_radius_min = Label(root, text="Radius Min:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	spot_setting["radius_min"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_spots_radius_max = Label(root, text="Radius Max:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	spot_setting["radius_max"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_spots_sampling_variation = Label(root, text="Variation:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	spot_setting["sampling_variation"] = Text(root, height=1, width=15, padx=1, pady=1)

	# Pixelization
	label_pixelization = Label(root, text="Pixelization Settings", font=("shanti",15,'bold'), height=1, width=20, padx=1, pady=1, bg="#132c33", fg="white")
	label_percentage = Label(root, text="percentage:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pixelization["percentage"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_pixelization_variation = Label(root, text="Variation:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pixelization["pixelization_variation"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_density_x = Label(root, text="Density X:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pixelization["density_x"] = Text(root, height=1, width=15, padx=1, pady=1)

	label_density_y = Label(root, text="Density Y:", font=("shanti",15,'bold'), height=1, width=10, padx=1, pady=1, bg="#132c33", fg="white")
	pixelization["density_y"] = Text(root, height=1, width=15, padx=1, pady=1)

	# Set Default values for parameters generation
	set_default_setting()
	# Display setting
	label_width.grid(		column=0, row=4, padx=10, pady=1, sticky=E)
	label_height.grid(		column=0, row=5, padx=10, pady=1, sticky=E)
	label_polygon_size.grid(column=0, row=6, padx=10, pady=1, sticky=E)
	label_color_bleed.grid( column=0, row=7, padx=10, pady=1, sticky=E)
	label_max_depth.grid(	column=0, row=8, padx=10, pady=1, sticky=E)
	
	pattern_setting["width"].grid(		column=1, row=4, padx=0, pady=1, sticky=W)
	pattern_setting["height"].grid(		column=1, row=5, padx=0, pady=1, sticky=W)
	pattern_setting["polygon_size"].grid(column=1, row=6, padx=0, pady=1, sticky=W)
	pattern_setting["color_bleed"].grid( column=1, row=7, padx=0, pady=1, sticky=W)
	pattern_setting["max_depth"].grid(	column=1, row=8, padx=0, pady=1, sticky=W)

	#Spots
	label_Spot.grid( 	  columnspan=2, column=2, row=4, padx=0, pady=1)
	label_spots_amount.grid(			column=2, row=5, padx=5, pady=1, sticky=E)
	label_spots_radius_min.grid(		column=2, row=6, padx=5, pady=1, sticky=E)
	label_spots_radius_max.grid(		column=2, row=7, padx=5, pady=1, sticky=E)
	label_spots_sampling_variation.grid(column=2, row=8, padx=5, pady=1, sticky=E)

	#Spots text
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
	submit_label = button(root, text="Generate", height=35, width=100,command=content_generator,
						  font=("Raleway",12,"bold"),bg="black",fg="white")
	submit_label.grid(column=5, row=9, sticky="W")

def remove_all():
    if messagebox.askokcancel("Restart", "Do you want to Restart?"):
        python = sys.executable
        os.execl(python, python, *sys.argv)

def display_color(color, row, column, pnt="\n00%"):
	btn_text = str(color+pnt)
	button_label = button(root, text=btn_text, height=100, width=100, command=lambda: delete_color(button_label,color),
							font=("Raleway",15), bg=color, fg="white")
	button_label.grid(column=column, row=row)
    

def delete_color(button_label,to_delete):
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
		idx=0
		for color in hexadecimal:
			if color in color_score.keys():
				display_color(color, 2, idx,  color_score[color])
			else:
				display_color(color, 2, idx)
			idx += 1
	else:
		messagebox.showinfo("Error while choosing colours", "Cannot load more than 7 colours, please delete first by clicking the colour buttons")
    

def extract_color(image):
	if image.mode != "RGB":
		image = image.convert("RGB")
	numpy_image = np.array(image) 
	# print(numpy_image.shape)
	width, height = numpy_image.shape[0:2]
	pixel = numpy_image.reshape((height*width , 3))

	km = MiniBatchKMeans( n_clusters = int(dominant_color.get()) )
	km.fit(pixel)
	minibatch_centers = np.array(km.cluster_centers_ , dtype='uint8')

	hexadecimal.clear()
	for array in minibatch_centers:
		hexadecimal.append( '#%02x%02x%02x' % (array[0], array[1], array[2]) )
	
	global score
	score = np.unique(km.labels_, return_counts=True)[1] 

	idx=0
	for color in hexadecimal:
		color_score[color] = "\n"+str(np.round( (score[idx]*100) / len(km.labels_),2)) + "%"
		display_color(color, 2, idx, color_score[color])
		idx += 1

	for color in choosen_color:
		display_color(color, 2, idx)
		idx += 1
	browse_text.set("Browse")
	


root = Tk()
root.title("Camflouge Generator")
root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10

#header area - logo & browse button
header = Frame(root, width=1200, height=175, bg="white")
header.grid(columnspan=8, rowspan=2, row=0)

color_content = Frame(root, width=1200, height=150, bg="#51c4d3")
color_content.grid(columnspan=8, rowspan=1, row=2)


#main content area - text and image extraction
# main_content = Frame(root, width=800, height=250, bg="#20bebe")
# main_content.grid(columnspan=3, rowspan=2, row=4)

def open_file():
	browse_text.set("loading...")
	# file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")])
	filename = askopenfilename()
	if filename:
		img = Image.open(filename) #.resize( Image.NEAREST(225, 225))) # the one-liner I used in my app
		# img = ImageTk.PhotoImage(img)
		# image_label = Label(root, image=img)
		# image_label.image = img # this feels redundant but the image didn't show up without it in my app
		extract_color(img)
		

# Display Logo
display_logo('chameleon.png', row=0, column=0, columnspan=2)
#instructions
instructions = Label(root, text="Select an Image", font=("Raleway", 15,'bold'), bg="white")
instructions.grid(column=7, row=0,columnspan=1, sticky=SE, padx=50, pady=5)

#browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), 
					font=("Raleway",12,'bold'), highlightbackground="#20bebe", 
					bg="#20bebe", fg="black", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=7, row=1,columnspan=1, sticky=NE, padx=50)

choose_color = Button(root, text="Pick a color", command=choose, 
						font=("Raleway",12), highlightbackground="#20bebe", 
						bg="#20bebe", fg="black", height=2, width=15)
choose_color.grid(column=5, row=1, sticky=NE)

dominant_color = StringVar(root)
dominant_color.set(5)
question_menu = OptionMenu(root, dominant_color, *options_list)
question_menu.grid(column=6, row=0, sticky=SE)

extraction_methon = StringVar(root)
extraction_methon.set("Terrain")
question_menu = OptionMenu(root, extraction_methon, *["Terrain", "Terrain with object"])
question_menu.grid(column=6, row=1, sticky=NE)

restart_app = Button(root, text="Restart App", command=remove_all, 
						font=("Raleway",12), highlightbackground="#20bebe", 
						bg="#20bebe", fg="black", height=2, width=15)
restart_app.grid(column=4, row=1, sticky=NE)

generate_btn = Button(root, text="Generate Pattern", command=generate_pattern, 
						font=("Raleway",12), highlightbackground="#20bebe", 
						bg="#20bebe", fg="black", height=2, width=15)
generate_btn.grid(column=7, row=2)



root.mainloop()
