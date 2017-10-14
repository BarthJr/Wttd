#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
from urllib import request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""
def sort_url(url):
    match = re.search(r'-(\w+)-(\w+)\.\w+', url)
    if match:
        return match.group(2)
    else:
        return url

def read_urls(filename):
    """Returns a list of the puzzle urls from the given log file,
    extracting the hostname from the filename itself.
    Screens out duplicate urls and returns the urls sorted into
    increasing order."""
    partial_url = "http://" + filename.split("_")[1]
    urls = set()
    puzzles = re.findall(r'GET (\S+puzzle\S+)', open(filename).read())

    for picture in puzzles:
        urls.add(partial_url + picture)

    return sorted(urls, key=sort_url)

def download_images(img_urls, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    #muda o diretorio corrente para o diretorio dest_dir
    os.chdir(dest_dir)

    img_tags = []

    for url in img_urls:
        img_name = url.split("/")[-1]
        # Por ter setado o diretorio corrente ali em cima não é necessario passar o caminho da imagem
        request.urlretrieve(url, img_name)
        img_tags.append(f'<img src="{img_name}">')

    # É passado o parametro w para escrever no arquivo, se não passar parametro, lê por padrão
    with open("index.html", "w") as f:
        f.write(f"<html><body>{''.join(img_tags)}</body></html>")

def main():
    args = sys.argv[1:]

    if not args:
        print('usage: [--todir dir] logfile ')
        sys.exit(1)

    todir = ''
    if args[0] == '--todir':
        todir = args[1]
        del args[0:2]

    img_urls = read_urls(args[0])
    print(img_urls)

    if todir:
        download_images(img_urls, todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main()
