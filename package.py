#!/usr/bin/python

# System: MacOS High Sierra
# Author: richard pct

"""Configure and install package"""

import os, shutil, urllib2, re, argparse, tarfile
from subprocess import Popen, PIPE, check_call, CalledProcessError
from importlib import import_module

workdir = "/tmp/build"

def clean_workdir(workdir, pkg_name):
    """clean workdir"""
    pkg_path = os.path.join(workdir, pkg_name)

    if os.path.isdir(pkg_path):
        shutil.rmtree(pkg_path)
    elif os.path.isfile(pkg_path):
        os.remove(pkg_path)
    elif not os.path.isdir(workdir):
        os.makedirs(workdir)

def checksum(hash_type, digest, pkg_file):
    """check file"""
    ret = True

    if hash_type == "sha256":
        p1 = Popen(["echo", digest + "  " + pkg_file], stdout=PIPE)
        p2 = Popen(["shasum", "-c"], stdin=p1.stdout, stdout=PIPE)
        p1.stdout.close()
        p2.communicate()
    else:
        print hash_type + " is not valid"
        exit(1)

    if p2.returncode != 0:
        ret = False

    return ret

def download_pkg(pkg_url, file_dest):
    """download package"""
    try:
        response = urllib2.urlopen(pkg_url)
    except urllib2.HTTPError:
        print "[Error] downloading: " + pkg_url
        exit(1)

    html = response.read()

    with open(file_dest, 'wb') as f:
        f.write(html)

def unpack(file_src):
    """unpack file"""
    extension = re.search(r'(tar\..*)', file_src)

    if extension == None:
        extension = re.search(r'\.(tgz)$', file_src)

    if extension == None:
        print "[Error]: package extension is not valid"
        exit(1)

    if extension.group(1) == "tar.xz":
        try:
            check_call(["tar", "xzf", file_src])
        except CalledProcessError:
            print "[Error] untar " + file_src
            exit(1)
    elif extension.group(1) in ("tar.gz", "tgz"):
        tar = tarfile.open(file_src)
        tar.extractall()
        tar.close()
    else:
        print "[Error]: extention package is not valid"
        exit(1)

def main():
    """main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--pkg",
                        choices=[ "libtool", "openssl", "autoconf",
                                  "automake", "libevent", "tmux", "tree"],
                        help="package to build and install",
                        required=True
                        )
    parser.add_argument("--destdir", help="install directory", required=True)
    args = parser.parse_args()
    pkg = import_module(args.pkg)
    destdir = args.destdir
    url_src = os.path.join(pkg.pkg_url, pkg.pkg_src)
    file_src = os.path.join(workdir, pkg.pkg_src)
    clean_workdir(workdir, pkg.pkg_name)

    if not checksum(pkg.hash_type, pkg.pkg_sha256, file_src):
        download_pkg(url_src, file_src)
        if not checksum(pkg.hash_type, pkg.pkg_sha256, file_src):
            print "[Error]: " + file_src + " is corrupted"
            exit(1)

    os.chdir(workdir)
    unpack(file_src)
    path_src = os.path.join(workdir, pkg.pkg_name)
    os.chdir(path_src)
    pkg.build(path_src, destdir)
    pkg.install(path_src, destdir)

if __name__ == '__main__':
    main()
