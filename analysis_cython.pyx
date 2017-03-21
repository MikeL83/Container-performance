# -*- coding: utf-8 -*-
"""

Synopsis

"""

#import numpy
import random
import cython
from cpython cimport array

def generateRandomList(int a, int b):
    random.seed()
    cdef list rand_list = [random.randint(1, b) for k in range(b)]
    return rand_list

def analysis_cython(int n):
    cdef array.array list_v = array.array('i',sorted(generateRandomList(1, n)))
    random.seed()
    cdef int rand_idx
    while len(list_v) != 0:
        rand_idx = random.randint(0, len(list_v) - 1)
        list_v.pop(rand_idx)
