from tkinter import *
from tkinter import ttk
from tkinter import colorchooser, messagebox
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfile
from functions import display_logo, display_textbox, extract_images, display_icon, resize_img, display_images 
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
dominant_color = 5
hexadecimal = []
choosen_color = []



def remove_all():
	if messagebox.askokcancel("Restart", "Do you want to Restart?"):
		python = sys.executable
		os.execl(python, python, *sys.argv)

def display_color(color, row, column):
	button_label = button(root, text=color, height=100, width=100, command=lambda: delete_color(button_label,color),
							font=("Raleway",15), bg=color, fg="white")
	button_label.grid(column=column, row=row)
	

def delete_color(button_label,to_delete):
	button_label.grid_forget()
	if to_delete in hexadecimal:
		hexadecimal.remove(to_delete)

	if to_delete in choosen_color:
		choosen_color.remove(to_delete)


	
def choose():
	add_color = colorchooser.askcolor()[1]
	hexadecimal.append(add_color)
	choosen_color.append(add_color)
	idx=0
	for color in hexadecimal:
		display_color(color, 2, idx)
		idx += 1
	


def extract_color(image):
	if image.mode != "RGB":
		image = image.convert("RGB")
	numpy_image = np.array(image) 
	# print(numpy_image.shape)
	width, height = numpy_image.shape[0:2]
	pixel = numpy_image.reshape((height*width , 3))

	km = MiniBatchKMeans( n_clusters = dominant_color)
	km.fit(pixel)
	minibatch_centers = np.array(km.cluster_centers_ , dtype='uint8')

	hexadecimal.clear()
	for array in minibatch_centers:
		hexadecimal.append( '#%02x%02x%02x' % (array[0], array[1], array[2]) )
	

	idx=0
	for color in hexadecimal:
		display_color(color, 2, idx)
		idx += 1

	for color in choosen_color:
		display_color(color, 2, idx)
		idx += 1
	browse_text.set("Browse")
	


root = Tk()
root.geometry('+%d+%d'%(350,10)) #place GUI at x=350, y=10

#header area - logo & browse button
header = Frame(root, width=1200, height=175, bg="white")
header.grid(columnspan=8, rowspan=2, row=0)

color_content = Frame(root, width=1200, height=250, bg="#20bebe")
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
instructions = Label(root, text="Select an Image", font=("Raleway", 10), bg="white")
instructions.grid(column=7, row=0,columnspan=1, sticky=SE, padx=75, pady=5)

#browse button
browse_text = StringVar()
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), 
					font=("Raleway",12), highlightbackground="#20bebe", 
					bg="#20bebe", fg="black", height=2, width=15)
browse_text.set("Browse")
browse_btn.grid(column=7, row=1,columnspan=1, sticky=NE, padx=50)

choose_color = Button(root, text="Pick a color", command=choose, 
						font=("Raleway",12), highlightbackground="#20bebe", 
						bg="#20bebe", fg="black", height=2, width=15)
choose_color.grid(column=7, row=2)

restart_app = Button(root, text="Restart App", command=remove_all, 
						font=("Raleway",12), highlightbackground="#20bebe", 
						bg="#20bebe", fg="black", height=2, width=15)
restart_app.grid(column=3, row=1, sticky=N)



root.mainloop()
