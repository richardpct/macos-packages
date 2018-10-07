#!/usr/bin/python

# Package: libtool
# System: MacOS High Sierra
# Author: richard pct

"""libtool"""

from subprocess import check_call, CalledProcessError

pkg_version = "2.4.6"
pkg_name = "libtool-" + pkg_version
pkg_src = pkg_name + ".tar.xz"
pkg_url = "http://ftpmirror.gnu.org/libtool"
hash_type = "sha256"
pkg_sha256 = "7c87a8c2c8c0fc9cd5019e402bed4292462d00a718a7cd5f11218153bf28b26f"

def build(path_src, destdir):
    """configure and make"""
    try:
        check_call(["./configure", "--prefix=" + destdir, "--program-prefix=g"])
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
