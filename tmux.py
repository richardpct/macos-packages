#!/usr/bin/python

# Package: tmux
# System: MacOS High Sierra
# Author: richard pct

"""tmux"""

from subprocess import check_call, CalledProcessError, Popen

pkg_version = "2.7"
pkg_name = "tmux-" + pkg_version
pkg_src = pkg_name + ".tar.gz"
pkg_url = "https://github.com/tmux/tmux/releases/download/" + pkg_version
hash_type = "sha256"
pkg_sha256 = "9ded7d100313f6bc5a87404a4048b3745d61f2332f99ec1400a7c4ed9485d452"

def build(path_src, destdir):
    """configure and make"""
    ldflags = "-L" + destdir + "/lib"
    cppflags = "-I" + destdir + "/include"
    p = Popen(["./configure", "--prefix=" + destdir],
               cwd = path_src,
               env = {"LDFLAGS": ldflags, "CPPFLAGS": cppflags})
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
