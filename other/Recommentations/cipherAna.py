
from aptx4869 import *
from statistic import *
from cluster import *
import sys
import re


all_data = []

def get_data(test):
    _f = open(test+".cipher","rb").read()
    data = dict.fromkeys([chr(i) for i in  range(256)],0)
    

    for i in _f:
        data[i] += 1

    return data.values()

def get_words(f):

    res = open(f).read()
    wor_re = re.compile(r'([\w\d_]+)')
    return wor_re.findall(res)

def test_encrypt(test_f,key):

    aptx4869(test_f,key,4)
    tmp_data = get_data(test_f)
    all_data.append(tmp_data)





wo = sys.argv[1]
words = [ wo for i in range(200)]
print "all : {}".format(len(words))
count = 0 
for k in words:
    test_encrypt(sys.argv[2],k)
    count += 1

    sys.stdout.write("now  : %+8d/%-8d \r"%( count,len(words)))
    sys.stdout.flush()



print all_data
print words
print len(all_data)
coords = scaledown(all_data)
print coords
print "\n ok "
draw2d(coords,words,jpg="/Users/darkh/Desktop/cipher.test.jpg")
