from tkinter import *
from PIL import Image, ImageTk
from tkmacosx import Button as button


#place an image on the grid
def display_logo(url, row, column,columnspan):
    img = Image.open(url)
    #resize image
    img = img.resize((int(img.size[0]/4.5),int(img.size[1]/4.5)))
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(column=column, row=row,columnspan=columnspan, rowspan=2, sticky=NW, padx=20, pady=40)

def display_icon(url, row, column, stick):
    icon = Image.open(url)
    #resize image
    icon = icon.resize((25,25))
    icon = ImageTk.PhotoImage(icon)
    icon_label = Button(image=icon, width=25, height=25)
    icon_label.image = icon
    icon_label.grid(column=column, row=row, sticky=stick)


#place a tebox on the pages
def display_textbox(content, ro, col, root):
    text_box = Text(root, height=10, width=30, padx=10, pady=10)
    text_box.insert(1.0, content)
    text_box.tag_configure("center", justify="center")
    text_box.tag_add("center", 1.0, "end")
    text_box.grid(column=col, row=ro, sticky=SW, padx=25, pady=25)

#Detect Images inside the PDF document
#Thank you sylvain of Stackoverflow
#https://stackoverflow.com/questions/2693820/extract-images-from-pdf-without-resampling-in-python
def extract_images(page):
    images = []
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                mode = ""
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "CMYK"
                img = Image.frombytes(mode, size, data)
                images.append(img)
    return images

def resize_img(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height:
        height = int( 300/width* height)
        width = 300
    elif height > width:
        width = int( 250/height * width)
        height = 250
    else:
        width, height = 250, 250

    img = img.resize((width,height))
    return img

def display_images(img):
    img = resize_img(img)
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="white")
    img_label.image = img
    img_label.grid(row=5, column=6, rowspan=4, columnspan=2)
    return img_label

def delete_color_option():
    value_inside = StringVar(root)
    # Set the default value of the variable
    value_inside.set("Delete a Color")
    delete_option = OptionMenu(root, value_inside, *hexadecimal)
    delete_option.grid(column=6, row=3, sticky=NE)

    delete_btn = Button(root, text="Delete", command=lambda:delete_color(value_inside), 
                        font=("Raleway",12), highlightbackground="#20bebe", 
                        bg="#20bebe", fg="black", height=1, width=15)
    delete_btn.grid(column=7, row=3, sticky=NW)


##########################################



