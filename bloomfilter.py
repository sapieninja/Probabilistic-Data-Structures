import sys
import random
import pyhash
#important variables for the bloom filter
length     = 10000000
k          = 4
saturation = 300000

hasher = pyhash.fnv1_64()

def newusername():
    return str(random.randint(0,10000000))
def gethash(data,i):
    # we split the hash into the first 32 bits and the second 32 bits
    value = hasher(data)
    second = value%4294967296
    value -= second
    first = value//4294967296
    return first + second*i #makes as many different hash functions as we want
def addtofilter(blm,k,data):
    for i in range(k):
        value = gethash(data,i) % length 
        changebyte = blm[value//8]
        mask = 1 << (7-(value%8))             #shifts one bit to the right place
        blm[value//8] = changebyte | mask   #bitwise OR
def checkfilter(blm,k,data):
    output = True
    for i in range(k):
        value = gethash(data,i) % length
        checkbyte = blm[value//8]
        mask = 1 << (7-value%8)
        checkbyte = checkbyte & mask        #bitwise AND
        if checkbyte == 0:
            output = False
    return output


blm = bytearray(length)
hashset = set()
#first we fill the kbloom filter
for x in range(saturation):
    toadd = newusername()
    hashset.add(toadd)
    addtofilter(blm,k,toadd)
print(sys.getsizeof(blm))
print(sys.getsizeof(hashset))
for x in hashset:
    if checkfilter(blm,k,x) == False:
        print("ERROR")
counter = 0
for x in range(1000000):
    if checkfilter(blm,k,newusername()) == True:
        counter += 1
print(counter/1000000)

