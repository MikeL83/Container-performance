# -*- coding: utf-8 -*-
"""

Synopsis

"""

import random


def generateRandomList(int a, int b):
    random.seed()
    cdef list rand_list = [random.randint(1, b) for k in range(b)]
    return rand_list

def analysis_cython(int n):
    cdef list list_v = generateRandomList(1, n)
    list_v.sort()
    random.seed()
    cdef int rand_idx
    while len(list_v) != 0:
        rand_idx = random.randint(0, len(list_v) - 1)
        list_v.pop(rand_idx)