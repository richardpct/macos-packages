#!/usr/bin/python

# Package: autoconf
# System: MacOS High Sierra
# Author: richard pct

"""autoconf"""

import fileinput, re
from subprocess import check_call, CalledProcessError

pkg_version = "2.69"
pkg_name = "autoconf-" + pkg_version
pkg_src = pkg_name + ".tar.gz"
pkg_url = "http://ftp.gnu.org/gnu/autoconf"
hash_type = "sha256"
pkg_sha256 = "954bd69b391edc12d6a4a51a2dd1476543da5c6bbf05a95b59dc0dd6fd4c2969"

def build(path_src, destdir):
    """configure and make"""
    pattern = re.compile(r"libtoolize")

    for line in fileinput.input("bin/autoreconf.in", inplace=True):
        new_line = pattern.sub("glibtoolize", line)
        print new_line.rstrip()

    try:
        check_call(["./configure", "--prefix=" + destdir])
    except CalledProcessError:
        print "[Error] configure"
        exit(1)

    try:
        check_call(["make"])
    except CalledProcessError:
        print "[Error] make"
        exit(1)

def install(path_src, destdir):
    """install"""
    try:
        check_call(["make", "install"])
    except CalledProcessError:
        print "[Error] make install"
        exit(1)
