import numpy as np
from math import sqrt 
from string import ascii_letters,punctuation ,digits
import os
from numpy.random import *

words_table  = [ascii_letters, punctuation, digits]


def pearson(v1,v2):

    E = lambda v1 : sum(v1) / len(v1)
    E_mul = lambda v1,v2 : sum( [ v1[i] * v2[i] for i in range(len(v1)) ]) /len(v1)
    D = lambda v1 : sum([(x  - E(v1))**2  for x  in v1 ]) /len(v1)

    std = lambda v1: sqrt(D(v1))

    num = len(v1)


    return   (E_mul(v1,v2) - E(v1) * E(v2)) / ( std(v1) * std(v2) )


def wordRandom(l):
    locate = [  [ randint(3) , randint(30) ]  for i in  range(l)]

    get = lambda m : words_table[m[0]][m[1] % len(words_table[m[0]])] 
    return ''.join(map(get,locate))

    


