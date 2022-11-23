import argparse
from collections import Counter
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import numpy as np

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

def HEX2RGB(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def colorz(img, origin, filename, outdir, parser, n=3):
    if parser.show:
        plt.imshow(origin)
        plt.show()
    img.thumbnail((200, 200))
    img = np.array(img.getdata()).reshape(img.size[0]*img.size[1], 3)
    clf = KMeans(n_clusters = n, init='k-means++')
    labels = clf.fit_predict(img)
    counts = Counter(labels)
    center_colors = clf.cluster_centers_
    hex_colors = [RGB2HEX(center_colors[i]) for i in counts.keys()]
    if parser.show:
        plt.scatter(img[:,0], img[:,1], c=labels)  
        plt.scatter(center_colors[:,0] , center_colors[:,1] , color = 'black')
        plt.show()
    create_palette(hex_colors, origin, filename, outdir, parser, n)

def paste_image(background, image):
    background.paste(image, (0,0))
    return ImageDraw.Draw(background)

def change_font(size,n):
    return ImageFont.truetype("OpenSans.ttf", int(round(size/n)/8))

def change_color_text(color):
    rgb = HEX2RGB(color)
    color_l = 0.2126*rgb[0]+0.7152*rgb[1]+0.0722*rgb[2]
    if(color_l/255 < 0.5):
        return '#ffffff'
    else:
        return '#000000'

def create_palette(colors, origin, filename, outdir, parser, n):
    img_w, img_h = origin.size
    background = None
    if img_w >= img_h:
        background = Image.new('RGB', (img_w, img_h+round(img_w/n)), (255, 255, 255))
        draw = paste_image(background, origin)
        cx = 0
        for i in range(len(colors)):
            draw.rectangle((cx, img_h+round(img_w/n), round(img_w/n)*(i+1), img_h), fill=colors[i])
            font = change_font(img_w,n)
            text_width, text_height = draw.textsize(colors[i], font)
            color_text = change_color_text(colors[i])
            draw.text(
                (cx+(round(img_w/n)/2)-(text_width/2),img_h+(round(img_w/n)/2)-(text_height/2)),
                colors[i],
                fill=color_text,
                font=font
            )
            cx += round(img_w/n)
    if img_h > img_w:
        background = Image.new('RGB', (img_w+round(img_h/n), img_h), (255, 255, 255))
        draw = paste_image(background, origin)
        cy = 0
        for i in range(len(colors)):
            draw.rectangle((img_w, cy, img_w+round(img_h/n), cy+round(img_h/n)), fill=colors[i])
            font = change_font(img_h,n)
            text_width, text_height = draw.textsize(colors[i], font)
            color_text = change_color_text(colors[i])
            draw.text(
                (img_w+(round(img_h/n)/2)-(text_width/2),cy+(round(img_h/n)/2)-(text_height/2)),
                colors[i],
                fill=color_text,
                font=font
            )
            cy += round(img_h/n)
    if parser.show:
        plt.imshow(background)
        plt.show()       
    background.save(outdir+filename)

def createParser ():
    parser = argparse.ArgumentParser(description='Palette colors from image')
    parser.add_argument('--show', type=bool, default=False, help='Show images')
    parser.add_argument('--indir', type=str, default="images/", help='Input dir for images')
    parser.add_argument('--outdir', type=str, default="palette/", help='Output dir for images')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    parser = createParser()
    files = os.listdir(parser.indir)
    for f in files:
        img = Image.open(parser.indir+f)
        origin = Image.open(parser.indir+f)
        colorz(img, origin, f, parser.outdir, parser, 5)