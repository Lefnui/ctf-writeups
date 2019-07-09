#!/usr/bin/env sage

from PIL import Image

#LGD mod 512
class LGD:
  def __init__(self, a, b, seed):
    self.a = a
    self.b = b
    self.state = seed
    self.p = 512

  def next(self):
    self.state = ((self.state * self.a) + self.b) % self.p
    return self.state

#From 3 points, extract the params of the LGD: a, b and seed
def getParams(points):
  r1, r2, r3 = points
  #Solutions are given in alphabetical order, so sort the variables
  var("a,b,seed")
  eqns = [r1 == seed*a + b, r2 == r1*a + b, r3 == r2*a + b]
  values = solve_mod(eqns=eqns, modulus=512, solution_dict=False)[0]
  #values are IntegerMod, we need to convert them to int
  return [int(v) for v in values]


#Parse image and gather pixels
img = Image.open('leHACK19_chall.png')
width, height = img.size
pixels = [ [img.getpixel((x, y)) for y in range(height)] for x in range(width)]

#Extract starting points
#Points have an alpha of 254
#We know the flag format is lehack 
#so first 3 characters are len
#based on our observations, characters
#are put in R, then G, then B, ...
#so we look for "l" in R, "e" in G and "h" in B
#Hopefully there are no dupplicates 
starting_points = [None for i in range(3)]
start = [ord(c) for c in "leh"]
for x in range(0, width):
  for y in range(75, height):
    p = pixels[x][y]
    if p[3] == 254:
      for i in range(3):
        if  p[i] == start[i]:
          print("[+] Found point %d at (%d, %d)"%(i, x, y))
          assert starting_points[i] == None, "[!] Point %d has dupplicate coordinates: (%x, %y)"%(i, x, y)
          starting_points[i] = (x, y)

for i in range(3):
  assert starting_points[i] != None, "[!] Point %d has not been found"%(i)

#Get the params and create the LGD
x_params = getParams([starting_points[i][0] for i in range(3)])
y_params = getParams([starting_points[i][1]-75 for i in range(3)])

x_lgd = LGD(*x_params)
y_lgd = LGD(*y_params)

#Find the flag
c = 0
flag = ""
for i in range(30):
  x, y = x_lgd.next(), y_lgd.next() + 75
  flag += chr(pixels[x][y][c])
  c = (c+1) % 3

print(flag)

