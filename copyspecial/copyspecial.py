#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Problem description:
# https://developers.google.com/edu/python/exercises/copy-special


import sys
import re
import os
import shutil
import zipfile

"""Copy Special exercise

"""


def get_paths(dir):
    if not os.path.exists(dir):
        error = f'Error: directory {dir} does not exist\n'
        sys.stderr.write(error)
        sys.exit(1)
    else:
        pattern = r'__(\w+)__'
        path_files = []
        for file in os.listdir(dir):
            match = re.search(pattern, file)
            if match:
                path_files.append(os.path.abspath(file))
    return path_files


def copy_files(orig, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)
    files = get_paths(orig)
    for file in files:
        shutil.copy(file, dest)


def zip_files(orig, filename):
    files = get_paths(orig)
    z = zipfile.ZipFile(filename, 'w')
    for file in files:
        z.write(os.path.basename(file))


# Write functions and modify main() to call them


def main():
    # This basic command line argument parsing code is provided.
    # Add code to call your functions below.

    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print("usage: [--todir dir][--tozip zipfile] dir [dir ...]")
        sys.exit(1)

    # todir and tozip are either set from command line
    # or left as the empty string.
    # The args array is left just containing the dirs.
    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    tozip = ''
    if args[0] == '--tozip':
        tozip = args[1]
        del args[0:2]

    if len(args) == 0:
        print("error: must specify one or more dirs")
        sys.exit(1)

    for arg in args:
        if todir:
            copy_files(arg, todir)
        if tozip:
            zip_files(arg, tozip)
        else:
            print('\n'.join(get_paths(arg)))
            # Call your functions


if __name__ == "__main__":
    main()
