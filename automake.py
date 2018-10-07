#!/usr/bin/python

# Package: automake
# System: MacOS High Sierra
# Author: richard pct

"""automake"""

import os
from subprocess import check_call, CalledProcessError, Popen

pkg_version = "1.16.1"
pkg_name = "automake-" + pkg_version
pkg_src = pkg_name + ".tar.xz"
pkg_url = "http://ftp.gnu.org/gnu/automake"
hash_type = "sha256"
pkg_sha256 = "5d05bb38a23fd3312b10aea93840feec685bdf4a41146e78882848165d3ae921"

def build(path_src, destdir):
    """configure and make"""
    path = os.environ["PATH"] + ":" + destdir + "/bin"
    p = Popen(["./configure", "--prefix=" + destdir],
               cwd = path_src,
               env = {"PATH": path})
    p.wait()

    if p.returncode != 0:
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
