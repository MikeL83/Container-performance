# -*- coding: utf-8 -*-
"""

Synopsis


"""

import argparse
import os
import pprint
import subprocess
import sys
import multiprocessing
import concurrent
import concurrent.futures
import logging
import time

CLANG_FORMAT = 'clang-format-4.0'
PYTHON_FORMATTER = 'yapf'
PYTHON_FORMATTER_OPTIONS = "{based_on_style: chromium, indent_width: 4, spaces_before_comment = 4," \
                           "split_before_logical_operator = true}"


class Logger:

    (DEBUG, INFO, WARNING, ERROR, CRITICAL) = ('debug', 'info', 'warning', 'error', 'critical')

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.INFO)

        # create a file handler
        # handler = logging.FileHandler('hello.log')
        # handler.setLevel(logging.INFO)
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        # add the handlers to the logger
        self._logger.addHandler(ch)

    def add_log(self, message, level):
        if level == self.DEBUG:
            self._logger.debug(message)
        elif level == self.INFO:
            self._logger.info(message)
        elif level == self.WARNING:
            self._logger.warning(message)
        elif level == self.ERROR:
            self._logger.error(message)
        elif level == self.CRITICAL:
            self._logger.critical(message)

def run_cmd(cmd):
    return subprocess.call(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           universal_newlines=True)


def get_files(path, formats, recur=False):
    if recur is False:
        if os.path.isdir(path):
            for file_ in os.listdir(path):
                if file_.lower().endswith(formats):
                    yield file_
    else:
        for root, dirs, files in os.walk(path):
            for file_ in files:
                if file_.lower().endswith(formats):
                    yield os.path.join(root, file_)


def wait_for(futures):
    canceled = False
    try:
        for future in concurrent.futures.as_completed(futures):
            err = future.exception()
            if err is None:
                pass
    except KeyboardInterrupt:
        canceled = True
        for future in futures:
            future.cancel()
        return canceled
    return canceled


def format_code(args):
    path = args['directory']
    lang = args['language']
    recur = args['recursive']
    concur = args['concurrency']
    if recur is False:
        path = path
        if lang == 'c++':
            if concur:
                futures = set()
                with concurrent.futures.ProcessPoolExecutor(
                        max_workers=multiprocessing.cpu_count()) as executor:
                    if os.path.isdir(path):
                        for file_ in get_files(path, ('.h', '.cpp')):
                            cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', file_)
                            future = executor.submit(run_cmd, cmd)
                    else:
                        sys.stderr.write('Given path is not a real directory!!\n')
                        raise SystemError(1)
                    futures.add(future)
                    canceled = wait_for(futures)
                    if canceled:
                        executor.shutdown()
            else:
                if os.path.isdir(path):
                    for file_ in get_files(path, ('.h', '.cpp')):
                        cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', file_)
                        res = run_cmd(cmd)
                else:
                    sys.stderr.write('Given path is not a real directory!!\n')
                    raise SystemError(1)
        else:
            if os.path.isdir(path):
                for file_ in get_files(path, ('.py', '.pyw')):
                    cmd = "{} {} {} {}".format(PYTHON_FORMATTER, '-i', '--style=' + PYTHON_FORMATTER_OPTIONS, file_)
                    res = run_cmd(cmd)
            else:
                sys.stderr.write('Given path is not a real directory!!\n')
                raise SystemError(1)
    else:
        if lang == 'c++':
            if concur:
                futures = set()
                with concurrent.futures.ProcessPoolExecutor(
                        max_workers=multiprocessing.cpu_count()) as executor:
                    if os.path.isdir(path):
                        for file_ in get_files(path, ('.h', '.cpp'), True):
                            cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', file_)
                            future = executor.submit(run_cmd, cmd)
                    else:
                        sys.stderr.write('Given path is not a real directory!!\n')
                        raise SystemError(1)
                    futures.add(future)
                    canceled = wait_for(futures)
                    if canceled:
                        executor.shutdown()
            else:
                if os.path.isdir(path):
                    for file_ in get_files(path, ('.h', '.cpp'), True):
                        cmd = "{} {} {} {}".format(CLANG_FORMAT, '-style=file', '-i', file_)
                        res = run_cmd(cmd)
                else:
                    sys.stderr.write('Given path is not a real directory!!\n')
                    raise SystemError(1)
        else:
            if os.path.isdir(path):
                for file_ in get_files(path, ('.py', '.pyw'), True):
                    cmd = "{} {} {} {}".format(PYTHON_FORMATTER, '-i', '--style=' + PYTHON_FORMATTER_OPTIONS, file_)
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
    ap.add_argument("-c", "--concurrency", type=bool,
                    default=False,
                    help="enable multiprocessing (default: False)")
    args = vars(ap.parse_args())
    return args


def main():
    args = parse_arguments()
    start = time.process_time()
    format_code(args)
    elapsed_time = time.process_time() - start

    print(elapsed_time)


if __name__ == "__main__":
    main()
