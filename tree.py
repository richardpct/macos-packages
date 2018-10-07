#!/usr/bin/python

# Package: tree
# System: MacOS High Sierra
# Author: richard pct

"""tree"""

import fileinput, re
from subprocess import check_call, CalledProcessError

pkg_version = "1.7.0"
pkg_name = "tree-" + pkg_version
pkg_src = pkg_name + ".tgz"
pkg_url = "http://mama.indstate.edu/users/ice/tree/src"
hash_type = "sha256"
pkg_sha256 = "35bd212606e6c5d60f4d5062f4a59bb7b7b25949"

def build(path_src, destdir):
    """configure"""
    pattern = re.compile(r'^(CFLAGS=-ggdb -Wall -DLINUX -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64)')

    for line in fileinput.input("Makefile", inplace=True):
        new_line = pattern.sub(r'#\1', line)
        print new_line.rstrip()

def install(path_src, destdir):
    """install"""
    cc = "cc"
    cflags = "-fomit-frame-pointer"
    ldflags = ""
    obj = "tree.o unix.o html.o xml.o json.o hash.o color.o strverscmp.o"
    mandir = destdir + "/share/man/man1"

    try:
        check_call(["make",
                    "prefix=" + destdir,
                    "CC=" + cc,
                    "CFLAGS=" + cflags,
                    "LDFLAGS=" + ldflags,
                    "OBJS=" + obj,
                    "mandir=" + mandir,
                    "install"])
    except CalledProcessError:
        print "[Error] make install"
        exit(1)
