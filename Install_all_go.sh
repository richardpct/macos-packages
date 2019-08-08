#!/bin/bash

set -e -u

packages="libtool openssl autoconf automake libevent tmux tree"

if [ "$#" -ne 1 ]; then
  echo "[Error]: need parameter for install destination"
  exit 1
fi

dest=$1

for package in $packages; do
  go get -u github.com/richardpct/macos-${package}
  macos-${package} -destdir=${dest}
done
