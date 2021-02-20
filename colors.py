import argparse
from collections import namedtuple
from math import sqrt
import random
import os
from PIL import Image, ImageDraw, ImageFont

Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(img, origin, filename, outdir, n=3):
    img_w, img_h = origin.size
    img.thumbnail((200, 200))
    points = get_points(img)
    clusters = kmeans(points, n, 1)  
    rgbs = [map(int, c.center.coords) for c in clusters]
    col = list(map(rtoh, rgbs))
    background = Image.new('RGB', (img_w, img_h+round(img_w/n)), (255, 255, 255))
    background.paste(origin, (0,0))
    draw = ImageDraw.Draw(background)
    cx = 0
    for i in range(len(col)):
        draw.rectangle((cx, img_h+round(img_w/n), round(img_w/n)*(i+1), img_h), fill=col[i])
        font = ImageFont.truetype("Montserrat-Medium.ttf", int(round(img_w/n)/8))#64
        rgb = hex_to_rgb(col[i])
        text_width, text_height = draw.textsize(col[i], font)
        color_text = '#ffffff'
        if(0.2126*rgb[0]+0.7152*rgb[1]+0.0722пш*rgb[2] < 0.5):
            color_text = '#ffffff'
        else:
            color_text = '#000000'
        draw.text(
            (cx+(round(img_w/n)/2)-(text_width/2),img_h+(round(img_w/n)/2)-(text_height/2)),
            col[i],
            fill=color_text,
            font=font
        )
        cx += round(img_w/n)             
    background.save(outdir+filename)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]
    while 1:
        plists = [[] for i in range(k)]
        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)
        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))
        if diff < min_diff:
            break
    return clusters

def hex_to_rgb(hex):
    h = hex.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def createParser ():
    parser = argparse.ArgumentParser(description='Palette colors from image')
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
        colorz(img, origin, f, parser.outdir, 5)