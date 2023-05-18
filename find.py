import argparse
import timeit
import fnmatch
import os
import sys
import re
import time
import logging
import doctest
from pathlib import Path

# Initialize logging
logging.basicConfig(filename='pyfind.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    parser = argparse.ArgumentParser(description="Find files matching specified criteria")
    parser.add_argument("path", nargs="*", default=".", help="Path(s) to search for files")
    parser.add_argument("-type", help="File is of type `type`")
    parser.add_argument("-atime", type=int, help="File was last accessed `n*24` hours ago")
    parser.add_argument("-group", help="File belongs to group `gname` (numeric group ID allowed)")
    parser.add_argument("-name", help="Base of file name matches shell pattern `pattern`")
    parser.add_argument("-regex", help="File name matches regular expression `pattern`")
    parser.add_argument("-newer", help="File was modified more recently than `file`")
    parser.add_argument("-version", action="version", version="%(prog)s 1.0")
    parser.add_argument("--test", action="store_true", help="Run automated unit tests")
    parser.add_argument("--benchmark", action="store_true", help="Run benchmark on core functions")
    args = parser.parse_args()

    command = " ".join(sys.argv)
    logging.info(f"{time.time()} {command}")

    if hasattr(args, "help") and args.help:
        parser.print_help()
        sys.exit()

    if args.test:
        doctest.testmod()

    if args.benchmark:
        print(timeit.timeit("search_files(args.path[0], '*', True)",setup="from __main__ import search_files, args",number=1000,))
        print(timeit.timeit("search_in_file('test.txt', 'hello', False)",setup="from __main__ import search_in_file",number=1000, ))
        sys.exit()

    # Implement find operation based on arguments
    matching_files = []
    for path in args.path:
        for root, dirs, files in os.walk(path):
            for name in files:
                filepath = os.path.join(root, name)
                if args.type and not os.path.isfile(filepath):
                    continue
                if args.atime:
                    access_time = os.path.getatime(filepath)
                    time_threshold = args.atime * 24 * 3600
                    last_access_limit = time.time() - time_threshold
                    if access_time > last_access_limit:
                        continue
                if args.group and args.group != os.stat(filepath).st_gid:
                    continue
                if args.name and not fnmatch.fnmatch(name, args.name):
                    continue
                if args.regex and not re.search(args.regex, filepath):
                    continue
                if args.newer and os.path.getmtime(filepath) <= os.path.getmtime(args.newer):
                    continue
                matching_files.append(filepath)

    # Print the matching file paths
    for filepath in matching_files:
        print(filepath)


if __name__ == "__main__":
    main()
