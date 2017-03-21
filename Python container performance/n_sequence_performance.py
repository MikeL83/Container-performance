# -*- coding: utf-8 -*-
"""

Synopsis

"""

import numpy as np
import random
import timeit
import time
import argparse
import threading, collections
from datetime import datetime
from analysis_cython import analysis_cython


#pure python
def generateRandomList(a, b):
    random.seed()
    rand_list = [random.randint(1, b) for k in range(b)]
    return rand_list


def analysis(n):
    list_v = generateRandomList(1, n)
    list_v.sort()
    random.seed()
    while len(list_v) != 0:
        rand_idx = random.randint(0, len(list_v) - 1)
        list_v.pop(rand_idx)


#numpy
def generateRandomArray(a, b):
    np.random.seed()
    rand_array = np.random.random_integers(1, b, b)
    return rand_array


def analysis_np(n):
    vec = generateRandomArray(1, n)
    vec.sort()
    np.random.seed()
    while vec.size != 0:
        rand_idx = np.random.random_integers(0, vec.size - 1)
        vec = np.delete(vec, rand_idx)


def parseArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n",
                    "--numberofelem",type=int,required=True,
                    help="number of conteiner elements")
    args = vars(ap.parse_args())
    return args['numberofelem']


if __name__ == "__main__":
    n = parseArgs()

    start = time.process_time()
    elapsed_time = 0.0
    times = []
    for k in range(3):
        start = time.process_time()
        t = threading.Thread(target=analysis, args=(n,))
        t.start()
        t.join()
        elapsed_time = time.process_time() - start
        times.append(elapsed_time)

    print("Execution time was {:.6f} s (best out of three)".format(min(times)))
