#!/usr/bin/env python3

from math import floor
import codecs
from itertools import cycle

H_ENGLISH = {
    ord(" "): 0.11502389,
    ord("e"): 0.112369492,
    ord("t"): 0.080162803,
    ord("a"): 0.072288091,
    ord("o"): 0.066448416,
    ord("i"): 0.061670501,
    ord("n"): 0.059723943,
    ord("s"): 0.056007786,
    ord("h"): 0.053884268,
    ord("r"): 0.052999469,
    ord("d"): 0.037603964,
    ord("l"): 0.035657406,
    ord("c"): 0.024597416,
    ord("u"): 0.024420457,
    ord("m"): 0.02132366,
    ord("w"): 0.02088126,
    ord("f"): 0.019731021,
    ord("g"): 0.017872943,
    ord("y"): 0.017430543,
    ord("p"): 0.017076624,
    ord("b"): 0.013183507,
    ord("v"): 0.008671032,
    ord("k"): 0.006812953,
    ord("j"): 0.001327199,
    ord("x"): 0.001327199,
    ord("q"): 0.000884799,
    ord("z"): 0.000619359
}

def xor(a, b):
    c = bytearray()
    for i in range(len(a)):
        c.append( a[i] ^b[i%len(b)])
    return c

def getBlock(b, k, n):
    out = bytearray()
    for i in range(k, len(b), n):
        out.append(b[i])
    return out

def getXORKey(b, histo=H_ENGLISH):
    freq = charFreq(b)
    comp = applyHistogram(freq, histo)
    return comp

def charFreq(b):
    freq = {}
    for i in b:
        if i not in freq:
            freq[i] = 0
        freq[i] += 1.0/len(b)
    return freq

def applyHistogram(uk_histo, ref_histo):
    uk_ordered =  sorted(uk_histo, key=uk_histo.__getitem__, reverse=True)
    matches = []
    M = 0
    key = uk_ordered[0]
    keys = {}
    for u in uk_ordered:
        for r in ref_histo.keys():
            k = u ^ r
            count = compareHistogram(uk_ordered, uk_histo, ref_histo, k)
            keys[k] = count
    keys_s =  sorted(keys, key=keys.__getitem__, reverse=True)
    return keys_s[0]

def compareHistogram(uk_keys, uk_values, ref, key):
    count = 0
    for u in uk_keys:
        x = u ^ key
        if x in ref.keys():
            count += uk_values[u] * ref[x]
    return count

cipher = codecs.decode("49380d773440222d1b421b3060380c3f403c3844791b202651306721135b6229294a3c3222357e766b2f15561b35305e3c3b670e49382c295c6c170553577d3a2b791470406318315d753f03637f2b614a4f2e1c4f21027e227a4122757b446037786a7b0e37635024246d60136f7802543e4d36265c3e035a725c6322700d626b345d1d6464283a016f35714d434124281b607d315f66212d671428026a4f4f79657e34153f3467097e4e135f187a21767f02125b375563517a3742597b6c394e78742c4a725069606576777c314429264f6e330d7530453f22537f5e3034560d22146831456b1b72725f30676d0d5c71617d48753e26667e2f7a334c731c22630a242c7140457a42324629064441036c7e646208630e745531436b7c51743a36674c4f352a5575407b767a5c747176016c0676386e403a2b42356a727a04662b4446375f36265f3f124b724c6e346544706277641025063420016629225b43432428036f29341a2338627c47650b264c477c653a67043e6766152a485c7f33617264780656537e5468143f305f4537722352303c3d4379043d69797e6f3922527b24536e310d653d4c33696c635474637d0326516f745e610d773340306621105a7361654e3e392970687c2e335f3015677d4b3a724a4659767c2f5b7c16055a126820306c14315d6b59224a27311f747f336f4d5974321a22507b22705a226c6d446a37375761423a2b5c29247163046d7e47032244377508300751727126326f117f7a38670c2b23203d4f27046a5c5e1532601126292f577776606f0c6d0126474b2a73737a41316362146e581d7c1228717664091c", "hex")

salt=b"WeAreDe1taTeam"
si =  cycle(salt)
unsalted = bytearray()

for c in cipher:
  unsalted.append(c ^ next(si))

for keysize in range(2, 38):
  key = bytearray()
  for i in range(keysize):
      block = getBlock(unsalted, i, keysize)
      k = getXORKey(block)
      key.append(k)

  print(keysize, "de1ctf{%s}"%(key.decode("ascii")))
  print(xor(unsalted, key))
