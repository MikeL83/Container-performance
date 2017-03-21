# -*- coding: utf-8 -*-
"""

Synopsis


"""

import argparse
import os
import pprint
import subprocess
import sys

CLANG_FORMAT = 'clang-format-4.0'
PYTHON_FORMATTER = 'yapf'
PYTHON_FORMATTER_OPTIONS = "{based_on_style: chromium, indent_width: 4, spaces_before_comment = 4," \
                           "split_before_logical_operator = true}"


def run_cmd(cmd):
    return subprocess.call(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          universal_newlines=True)


def format_code(args):
    if args['recursive'] is False:
        path = args['directory']
        if args['language'] == 'c++':
            if os.path.isdir(path):
                for file_ in os.listdir(path):
                    if file_.lower().endswith(('.h', '.cpp')):
                        cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', file_)
                        res = run_cmd(cmd)
            else:
                sys.stderr.write('Given path is not a real directory!!\n')
                raise SystemError(1)
        else:
            if os.path.isdir(path):
                for file_ in os.listdir(path):
                    if file_.lower().endswith(('.py', '.pyw')):
                        cmd = "{} {} {} {}".format(PYTHON_FORMATTER, '-i', '--style=' + PYTHON_FORMATTER_OPTIONS, file_)
                        res = run_cmd(cmd)
            else:
                sys.stderr.write('Given path is not a real directory!!\n')
                raise SystemError(1)
    else:
        path = args['directory']
        if args['language'] is 'c++':
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    for file_ in files:
                        if file_.lower().endswith(('.h', '.cpp')):
                            cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', os.path.join(root, file_))
                            res = run_cmd(cmd)
            else:
                sys.stderr.write('Given path is not a real directory!!\n')
                raise SystemError(1)


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-l",
                    "--language",
                    default='c++',
                    help="Programming language to be formatted. Possible values are C++ or Python (default is c++)")
    ap.add_argument("-d",
                    "--directory",
                    default='.',
                    help="Directory to  (default: current directory)")
    ap.add_argument("-r",
                    "--recursive",
                    default=False,
                    help="Format files recursively (default: false)")
    args = vars(ap.parse_args())
    return args


if __name__ == "__main__":
    args = parse_arguments()
    format_code(args)
