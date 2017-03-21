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

def run(n, style):
    elapsed_time = 0.0
    times = []
    runs = 5
    if n > 10000:
        runs = 2
    if style == 'pure':
        for k in range(runs):
            start = time.process_time()
            t = threading.Thread(target=analysis, args=(n,))
            t.start()
            t.join()
            elapsed_time = time.process_time() - start
            times.append(elapsed_time)
    elif style == 'numpy':
        for k in range(runs):
            start = time.process_time()
            t = threading.Thread(target=analysis_np, args=(n,))
            t.start()
            t.join()
            elapsed_time = time.process_time() - start
            times.append(elapsed_time)
    else:
        for k in range(runs):
            start = time.process_time()
            t = threading.Thread(target=analysis_cython, args=(n,))
            t.start()
            t.join()
            elapsed_time = time.process_time() - start
            times.append(elapsed_time)

    #print("Execution time was {:.6f} s (avg out of five)".format(np.mean(
    #    times)))
    return np.mean(times)

def parseArgs():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n",
                    "--numberofelem",
                    type=int,
                    required=True,
                    help="number of conteiner elements")
    ap.add_argument("-s",
                    "--style",
                    required=True,
                    help="Which python style to use")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    n = parseArgs()

    run(n['numberofelem'], n['style'])

