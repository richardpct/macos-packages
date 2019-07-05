#!/usr/bin/python

# Package: openssl
# System: MacOS High Sierra
# Author: richard pct

"""openssl"""

from subprocess import check_call, CalledProcessError

pkg_version = "1.0.2o"
pkg_name = "openssl-" + pkg_version
pkg_src = pkg_name + ".tar.gz"
pkg_url = "https://www.openssl.org/source"
hash_type = "sha256"
pkg_sha256 = "ec3f5c9714ba0fd45cb4e087301eb1336c317e0d20b575a125050470e8089e4d"

def build(path_src, destdir):
    """configure and make"""
    try:
        check_call(["/usr/bin/perl",
                    "./Configure",
                    "darwin64-x86_64-cc",
                    "--prefix=" + destdir,
                    "--openssldir=" + destdir + "/etc/openssl"])
    except CalledProcessError:
        print "[Error] configure"
        exit(1)

    try:
        check_call(["make", "depend"])
    except CalledProcessError:
        print "[Error] make depend"
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
