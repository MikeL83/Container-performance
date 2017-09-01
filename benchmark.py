# -*- coding: utf-8 -*-
"""

Synopsis


"""

import argparse
import os
import pprint
import subprocess
import sys
import re
from pprint import pprint
import json
import nsequencebench

COMPILERS = ('gcc', 'clang')
CONTAINERS = ('std::vector', 'std::list', 'std::forward_list',
              'boost::vector', 'boost::list', 'boost::slist',
              'boost::stable_vector')
LANGUAGES = ('c++', 'python')
SIZES = (10, 100, 1000, 10000, 50000) #, 100000, 200000, 500000, 1000000)
PYTHON_METHODS = ('pure', 'numpy', 'cython')
DB = {'c++': {'gcc': {}, 'clang': {}}, 'python': {}}


def run_cmd(cmd):
    return subprocess.check_output(cmd, shell=True, executable='/bin/bash', stderr=subprocess.STDOUT,
                                   universal_newlines=True)


def run_benchmark():
    # cmd = "{}".format("sudo -s")
    # res = run_cmd(cmd)
    regex = re.compile(r'(\d+[.]{1}\d+[eE]?[+-]?\d*)')
    for lang in LANGUAGES:
        if lang == 'python':
            for method in PYTHON_METHODS:
                results = []
                for size in SIZES:
                    # run benchmark
                    # cmd = "{} -n {} -s {}".format('python3 nsequencebench.py', size, method)
                    # res = run_cmd(cmd)
                    # time = regex.findall(res)
                    res = nsequencebench.run(size, method)
                    results.append(res)
                DB["python"][method] = results
        elif lang == 'c++':
            for compiler in COMPILERS:
                if compiler == 'gcc':
                    cmd = "{}".format("make clean && make -f gcc.mk")
                    res = run_cmd(cmd)
                    for cont in CONTAINERS:
                        results = []
                        for size in SIZES:
                            # run benchmark
                            cmd = "{} {} {}".format('./nsequencebench', size, cont)
                            res = run_cmd(cmd)
                            time = regex.findall(res)
                            results.append(float(time[0]))

                            if size < 50000:
                                cmd = "{} {} {} {} {}".format('sudo perf stat $(cat perf_options.txt) ./nsequencebench',
                                                              size, cont, '2>',
                                                              'perf_logs/gcc_' + cont + '_N' + str(size) + '_perf.data')
                            else:
                                cmd = "{} {} {} {} {}".format('sudo perf stat $(cat perf_options2.txt) ./nsequencebench',
                                                              size, cont, '2>',
                                                              'perf_logs/gcc_' + cont + '_N' + str(size) + '_perf.data')
                            res = run_cmd(cmd)

                        DB["c++"]["gcc"][cont] = results
                else:
                    cmd = "{}".format("make clean && make -f clang.mk")
                    res = run_cmd(cmd)
                    for cont in CONTAINERS:
                        results = []
                        for size in SIZES:
                            # run benchmark
                            cmd = "{} {} {}".format('./nsequencebench', size, cont)
                            res = run_cmd(cmd)
                            time = regex.findall(res)
                            results.append(float(time[0]))

                            if size < 50000:
                                cmd = "{} {} {} {} {}".format('sudo perf stat $(cat perf_options.txt) ./nsequencebench',
                                                              size, cont, '2>',
                                                              'perf_logs/clang_' + cont + '_N' + str(size) + '_perf.data')
                            else:
                                cmd = "{} {} {} {} {}".format('sudo perf stat $(cat perf_options2.txt) ./nsequencebench',
                                                              size, cont, '2>',
                                                              'perf_logs/clang_' + cont + '_N' + str(size) + '_perf.data')
                            res = run_cmd(cmd)
                        DB["c++"]["clang"][cont] = results
    with open('benchmark_results.json', 'w') as f:
        json.dump(DB, f)
        # analyze with perf


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-p",
                    "--password",
                    default='',
                    help="Your password for sudo")
    args = vars(ap.parse_args())
    return args


def main():
    args = parse_arguments()
    sudo_password = args['password']

    p = subprocess.Popen(['sudo', '-s'], stdin=subprocess.PIPE, stderr=subprocess.PIPE,
                         universal_newlines=True)
    sudo_prompt = p.communicate(sudo_password + '\n')[1]
    cmd = "{}".format("rm -r perf_logs && mkdir perf_logs")
    res = run_cmd(cmd)
    run_benchmark()

if __name__ == "__main__":
    main()
