# coding:utf
from PIL import Image, ImageDraw # модули из PIL
import os
# from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import io

def histogram_image(filename, channel_data, color, title):
    """Generate a histogram image for a single channel"""
    fig, ax = plt.subplots(figsize=(6,4))
    ax.hist(channel_data.ravel(), bins=256, range=(0,256), color=color)
    ax.set_title(title)
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    with open(filename, "wb") as f:
        f.write(buf.getbuffer())
    return filename

def histo(dir_name,prefix,file_name):
    os.makedirs(dir_name, exist_ok=True)
    # Load image with PIL
    img = Image.open(file_name).convert("RGB")
    img_np = np.array(img)

    # Extract channels
    r = img_np[:,:,0]
    g = img_np[:,:,1]
    b = img_np[:,:,2]
    gray = np.dot(img_np[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)

    hist_list = []
    # Create separate histogram images
    hist_list += [("red",histogram_image(dir_name + "/" + prefix + "_red_hist.png",r, "red", "Red Channel Histogram"))]
    hist_list += [("green",histogram_image(dir_name + "/" + prefix + "_green_hist.png",g, "green", "Green Channel Histogram"))]
    hist_list += [("blue",histogram_image(dir_name + "/" + prefix + "_blue_hist.png",b, "blue", "Blue Channel Histogram"))]
    hist_list += [("lum",histogram_image(dir_name + "/" + prefix + "_gray_hist.png",gray, "black", "Luminosity Histogram"))]

    return hist_list
