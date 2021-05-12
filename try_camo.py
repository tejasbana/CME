from tkinter import *
import numpy
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename

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


root = Tk()
root.title("Images, Exit buttons")

# image_list = []

# for i in range(3):

# 	# Load and Display Image: 3 steps
# 	my_img = ImageTk.PhotoImage( Image.open("./images/"+ str(i+1) + ".png"))
# 	# my_label = Label(image=my_img)
# 	# my_label.pack()

# 	image_list.append(my_img)


# Current image index and length of image list
my_img = ImageTk.PhotoImage( Image.open("./images/download.jpeg"))

# Display first image
image_label = Label(image=my_img)
image_label.grid(row=0, column=0, columnspan=3)


def next_image(image_number):
	global image_label
	global button_next
	global button_prev

	image_label.grid_forget()

	image_label = Label(image=image_list[image_number - 1])
	button_prev = Button(root, text="<<", command=lambda: prev_image(image_number-1))
	button_next = Button(root, text=">>", command=lambda: next_image(image_number+1))

	if image_number == 3:
		button_next = Button(root, text=">>", command=DISABLED)


	image_label.grid(row=0, column=0, columnspan=3)
	button_prev.grid(row=1, column=0)
	button_next.grid(row=1, column=2)


def prev_image(image_number):
	global image_label
	global button_next
	global button_prev

	image_label.grid_forget()

	image_label = Label(image=image_list[image_number - 1])
	button_prev = Button(root, text="<<", command=lambda: prev_image(image_number-1))
	button_next = Button(root, text=">>", command=lambda: next_image(image_number+1))

	if image_number == 1:
		button_prev = Button(root, text="<<", command=DISABLED)


	image_label.grid(row=0, column=0, columnspan=3)
	button_prev.grid(row=1, column=0)
	button_next.grid(row=1, column=2)

def upload_img():
	global image_label
	global button_next
	global button_prev

	image_label.grid_forget()

	filename = askopenfilename()
	img = ImageTk.PhotoImage(Image.open(filename)) #.resize( Image.NEAREST(225, 225))) # the one-liner I used in my app
	image_label = Label(root, image=img)
	image_label.image = img # this feels redundant but the image didn't show up without it in my app
	image_label.grid(row=0, column=0, columnspan=3)

	
	button_prev = Button(root, text="<<", command=lambda: prev_image(image_number-1))
	button_next = Button(root, text=">>", command=lambda: next_image(image_number+1))

	# image_label.grid(row=0, column=0, columnspan=3)
	button_prev.grid(row=1, column=0)
	button_next.grid(row=1, column=2)


# Buttons
button_prev = Button(root, text="<<", command=lambda: next_image(1))
button_upload = Button(root, text="Exit Program", command=upload_img)
button_next = Button(root, text=">>", command=lambda: next_image(2))

# Display buttons 
button_prev.grid(row=1, column=0)
button_upload.grid(row=1, column=1)
button_next.grid(row=1, column=2)


	


# def generate_pattern(img):
# 	dominant_color = 5
# 	hexa_colors = []
# 	x_end , y_end = img.shape[0:2]
#     pixel = img.reshape((x_end*y_end , 3))
#     km = MiniBatchKMeans( n_clusters = dominant_color)
#     km.fit(pixel)
#     minibatch_centers = km.cluster_centers_
#     minibatch_centers = np.array(minibatch_centers , dtype='uint8')

#     for array in minibatch_centers:
#         hexa_colors.append( '#%02x%02x%02x' % (array[0], array[1], array[2]) )

#     i =1
#     plt.figure(0,figsize=(8,2))

#     color = []
#     for x in minibatch_centers:
#         plt.subplot(1,5,i)
#         plt.axis("off")
#         i+=1
#         color.append(x)
        
#         a = np.zeros((100,100,3),dtype='uint8')
#         a[:,:,:] = x
#         plt.imshow(a)
#     # plt.imsave("generated/1"+str(request.files['photo'].filename))
    


#     parameters = {'width': 1080, 'height': 1080, 'polygon_size': 5, 'color_bleed': 5,'max_depth':8,
#           'colors': hexa_colors,
#           'spots': {'amount': 20000, 'radius': {'min': 10, 'max': 40}, 'sampling_variation': 10},
#           'pixelize': {'percentage': 1, 'sampling_variation': 20, 'density': {'x': 1500, 'y': 1500}} }


#     generated_image = generate(parameters)

root.mainloop()