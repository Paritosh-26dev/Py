import argparse
import fnmatch
import os
import sys
import re
import time
import logging
from pathlib import Path

LOG_FILENAME = str(Path.home() / '.find.py.log')
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description='Find files matching specified criteria')
    parser.add_argument('-type', help='File is of type `type`')
    parser.add_argument('-atime', type=int, help='File was last accessed `n*24` hours ago')
    parser.add_argument('-group', help='File belongs to group `gname` (numeric group ID allowed)')
    parser.add_argument('-name', help='Base of file name matches shell pattern `pattern`')
    parser.add_argument('-regex', help='File name matches regular expression `pattern`')
    parser.add_argument('-newer', help='File was modified more recently than `file`')
    parser.add_argument('-version', action='version', version='%(prog)s 1.0')
    parser.add_argument('--test', action='store_true', help='Run automated unit tests')
    parser.add_argument('--benchmark', action='store_true', help='Run benchmark on core functions')
    args = parser.parse_args()

    command = ' '.join(sys.argv)
    logging.info(f'{time.time()}] {sys.argv[0]} {command}')

    if args.help:
        parser.print_help()
        sys.exit()

    if args.test:
        run_tests()
        sys.exit()

    if args.benchmark:
        run_benchmark()
        sys.exit()

    #  implement find operation based on arguments
    for root, dirs, files in os.walk('.'):
        for name in files:
            if args.type and not os.path.isfile(name):
                continue
            if args.atime and (time.time() - os.path.getatime(name)) // (24 * 3600) != args.atime:
                continue
            if args.group and args.group != os.stat(name).st_gid:
                continue
            if args.name and not fnmatch.fnmatch(name, args.name):
                continue
            if args.regex and not re.match(args.regex, os.path.join(root, name)):
                continue
            if args.newer and os.path.getmtime(name) <= os.path.getmtime(args.newer):
                continue
            print(os.path.join(root, name))

def run_tests():
    # implement automated tests
    pass

def run_benchmark():
    # implement benchmark
    pass

