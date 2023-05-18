import argparse
import logging
import datetime
import fnmatch
import os
import re
import sys
import time

# Returns a list of files under the given directory path that match the given pattern. Performs recurrsive as well
def search_files(directory_path, pattern, recursive):
    if not os.path.isdir(directory_path):
        print(f"grep.py: {directory_path}: No such directory")
        return []

    files = []
    for root, _, filenames in os.walk(directory_path):
        for filename in filenames:
            if fnmatch.fnmatch(filename, pattern):
                files.append(os.path.join(root, filename))
        if not recursive:
            break

    return files

def search_in_file(file_path, regex, print_line_numbers):
    """
    Searches for regex in the given file.
    If print_line_numbers is True, prints the line numbers along with the matching lines.
    """
    try:
        with open(file_path) as f:
            for i, line in enumerate(f):
                if re.search(regex, line):
                    if print_line_numbers:
                        print(f"{file_path}:{i+1}:{line.rstrip()}")
                    else:
                        print(line.rstrip())
    except:
        print(f"grep.py: {file_path}: Permission denied")

def grep(pattern, directory_path, recursive, print_line_numbers, count_only, files_with_matches_only, include_pattern, exclude_pattern):
    """
    Searches for the given pattern in files under the given directory path.
    If recursive is True, the search is performed recursively.
    If print_line_numbers is True, prints the line numbers along with the matching lines.
    If count_only is True, prints only the count of matching lines in each file.
    If files_with_matches_only is True, prints only the names of the files with matching lines.
    The search is limited to files that match the include_pattern and do not match the exclude_pattern.
    """
    files = []
    if os.path.isfile(directory_path):
        files = [directory_path]
    else:
        files = search_files(directory_path, include_pattern or "*", recursive)
        if exclude_pattern:
            files = [file for file in files if not fnmatch.fnmatch(file, exclude_pattern)]

    match_count = 0
    for file in files:
        try:
            with open(file) as f:
                file_match_count = 0
                for line in f:
                    if re.search(pattern, line):
                        file_match_count += 1
                        match_count += 1

                        if files_with_matches_only:
                            print(file)
                            break
                        elif not count_only:
                            if print_line_numbers:
                                print(f"{file}:{file_match_count}:{line.rstrip()}")
                            else:
                                print(line.rstrip())
                if count_only:
                    print(f"{file}:{file_match_count}")
        except:
            print(f"grep.py: {file}: Permission denied")

    if count_only and len(files) > 1:
        print(f"Total matches: {match_count}")

    with open(os.path.expanduser("pygrep.log"), "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_cmd = " ".join(sys.argv)
        log_file.write(f"[{timestamp}] {full_cmd}\n")

def main():
    # configure logging
    logging.basicConfig(filename='pygrep.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # log the command-line arguments
    command = " ".join(sys.argv)
    logging.info(f"{time.time()} {command}")
    
    parser = argparse.ArgumentParser(description="Search for a pattern in files.")
    parser.add_argument("pattern", help="pattern to search for")
    parser.add_argument("path", nargs="?", default=".", help="directory or file to search in (default: current directory)")
    parser.add_argument("-c", "--count", action="store_true", help="print only a count of matching lines per file")
    parser.add_argument("-l", "--files-with-matches", action="store_true", help="print only names of FILEs containing matches")
    parser.add_argument("-n", "--line-number", action="store_true", help="print line number with output lines")
    parser.add_argument("-R", "-r", "--recursive", action="store_true", help="search files recursively")
    parser.add_argument("--include", help="search only files that match the specified pattern")
    parser.add_argument("--exclude", help="skip files and directories matching the specified pattern")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0")
    parser.add_argument("--test", action="store_true", help="run automated unit tests")
    parser.add_argument("--benchmark", action="store_true", help="run benchmark on core functions")

    args = parser.parse_args()

    if args.test:
        import doctest
        doctest.testmod()
        return

    if args.benchmark:
        import timeit
        print(timeit.timeit("search_files('.', '*', True)", setup="from __main__ import search_files", number=1000))
        print(timeit.timeit("search_in_file('test.txt', 'hello', False)", setup="from __main__ import search_in_file", number=1000))
        return

    pattern = args.pattern
    directory_path = args.path
    recursive = args.recursive
    print_line_numbers = args.line_number
    count_only = args.count
    files_with_matches_only = args.files_with_matches
    include_pattern = args.include
    exclude_pattern = args.exclude

    grep(pattern, directory_path, recursive, print_line_numbers, count_only, files_with_matches_only, include_pattern, exclude_pattern)

if __name__ == '__main__':
    main()
