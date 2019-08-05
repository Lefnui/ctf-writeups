#!/usr/bin/env python3 

import hashlib

#Script is available here: https://raw.github.com/bozhu/BMA/master/bma.py
from bma import Berlekamp_Massey_algorithm

class lfsr():
    def __init__(self, init, mask, length):
        self.init = init
        self.mask = mask
        self.lengthmask = 2**(length+1)-1

    def next(self):
        nextdata = (self.init << 1) & self.lengthmask 
        i = self.init & self.mask & self.lengthmask 
        output = 0
        while i != 0:
            output ^= (i & 1)
            i = i >> 1
        nextdata ^= output
        self.init = nextdata
        return output

#Use Berlekamp Massey to recover taps
#Output is a polynomial of form x^16 + x^14 + x^13 + x^11 + 1
#Turn it into a mask
def getMask(output):
  bm = Berlekamp_Massey_algorithm(output)
  coeffs = bm[0].split(" + ")[1:]
  length = bm[1]
  mask = 0
  for c in coeffs:
    if c == "1": 
      n = 0
    elif c == "x":
      n = 1
    else:
      n = int(c[2:])
    mask |= 1 << ((length - 1) -n)

  return mask, length

def check(seed):
  h = hashlib.sha256(b"%x"%seed).hexdigest()
  return h if h[:4] == "1224" else None

#Parse output
output = [int(c) for c in open("output").read()]

#Recover taps
mask = getMask(output)

"""
Output is 504 bits, which gives us a polynomial of degree 253.
In the task, there's an assert stating that degree is 256.
In the worst case we need 256*2 = 512 bits to recover the taps.
Bruteforce the remaining 8 bits to recover the original mask and the invert the LFSR
"""
for i in range(256):

  #Append 8 bits and recover mask
  n = [(i>>j)&1 for j in range(8)]
  mask, length = getMask(output + n)

  #Make sure degree is 256
  if length != 256 or mask.bit_length() != 256:
    continue

  #Get the state after 256 iterations from the 256 first output
  state = 0
  for i in range(length):
    state |= output[i] << (length - 1 - i) 
 
  #Invert the LFSR 
  for i in range(length):
    bit = state & 1 #expected_bit
    tmp = mask & (state >> 1)
   
    while tmp:
      bit ^= (tmp & 1) 
      tmp = tmp >> 1

    state = (state >> 1) | (bit << (length-1))

  #Checks that the mask and initial state yield the same output
  l = lfsr(state, mask, length) 
  valid = True
  for j in range(len(output)):
    valid &= (output[j] == l.next())

  #Checks that it is the right seed
  if valid:
    h = check(state)
    if h:
      print("Flag: de1ctf{%s}"%h)
      break
