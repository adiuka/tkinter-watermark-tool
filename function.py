import os, sys
from PIL import Image, ImageFont, ImageDraw
import matplotlib.pyplot as plt
import numpy as np

original_path = 'Tkinter-build/images/audrius.jpeg'
water_mark_path = 'Tkinter-build/assets/storm_works.png'

def img_watermark(image_path, watermark_path):

    im = Image.open(image_path) # Opens the original uploaded image to be modified
    water_mark = Image.open(watermark_path).convert("RGBA") # The conversion makes it more managable


    copied_im = im.copy() # Important not to mess with original image
    # pastes a watermark onto the image, (file, (coordinates) file again to make it transparent)
    copied_im.paste(water_mark, (int(im.width / 2 - water_mark.width / 2) , int(im.height / 2 - water_mark.height / 2)), water_mark) 
    filename = os.path.basename(im.filename) # Finds the file name of the path
    filename = filename.split(".")[0] # Splits it so it doesnt have the file type
    file_path = f"./created_images/{filename}_img_modified.jpeg"
    copied_im.save(file_path) # Allows you to save an image in a new format.


    # im.show() # Is used to open and show the image, need to have a reader installed.
    plt.imshow(copied_im) # Creates the image object for PLT
    plt.show() # Shows the image in PLT


def text_watermark(image_path, text):

    im = Image.open(image_path) # once again open the path
    watermark_im = im.copy() # We make a copy not to mess with the original

    draw = ImageDraw.Draw(watermark_im) # We apply our draw object

    width, height = im.size # Captures the height and size of the image
    x, y = int(width / 2), int(height / 2) # Captures the x and y for our font sizes and image coordinates
    if x > y:
        font_size = y
    elif y > x:
        font_size = x
    else:
        font_size = x

    font = ImageFont.truetype('arial.ttf', int(font_size / 6))

    draw.text((x, y), text, fill = (255, 255, 255), font = font, anchor='ms')
    filename = os.path.basename(im.filename) # Finds the file name of the path
    filename = filename.split(".")[0] # Splits it so it doesnt have the file type
    watermark_im.save(f"./created_images/{filename}_text_modified.jpeg") # Allows you to save an image in a new format.

    # im.show() # Is used to open and show the image, need to have a reader installed.
    plt.imshow(watermark_im)
    plt.show()


