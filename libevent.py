#!/usr/bin/python

# Package: libevent
# System: MacOS High Sierra
# Author: richard pct

"""libevent"""

import os
from subprocess import check_call, CalledProcessError, Popen

pkg_version = "2.1.8-stable"
pkg_name = "libevent-" + pkg_version
pkg_src = pkg_name + ".tar.gz"
pkg_url = "https://github.com/libevent/libevent/releases/download/release-2.1.8-stable"
hash_type = "sha256"
pkg_sha256 = "965cc5a8bb46ce4199a47e9b2c9e1cae3b137e8356ffdad6d94d3b9069b71dc2"

def build(path_src, destdir):
    """configure and make"""
    path = os.environ["PATH"] + ":" + destdir + "/bin"
    p1 = Popen(["./autogen.sh"],
               cwd = path_src,
               env = {"PATH": path})
    p1.wait()

    if p1.returncode != 0:
        print "[Error] autogen"
        exit(1)

    cppflags = "-I" + destdir + "/include"
    p2 = Popen(["./configure", "--prefix=" + destdir],
               cwd = path_src,
               env = {"CPPFLAGS": cppflags})
    p2.wait()

    if p2.returncode != 0:
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
