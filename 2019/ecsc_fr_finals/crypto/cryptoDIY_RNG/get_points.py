#!/usr/bin/env python


from PIL import Image

img = Image.open('leHACK19_chall.png')
pixels = list(img.getdata())
width, height = img.size
pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

pixels = [ [img.getpixel((x, y)) for y in range(height)] for x in range(width)]


for x in range(0, width):
  for y in range(75, height):
    p = img.getpixel((x, y))
    p = pixels[x][y]

    if p[3] == 254:
      print(x, y, [chr(c) for c in p[:3]])
