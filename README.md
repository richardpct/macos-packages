# macos-packages
My macOS packages

# Requirements
- macOS
- Go compiler

# Purpose
I do not use Homebrew because I want to install all my packages in my
environment user.  
I wrote a Makefile that retrieves my programs written in Go, then build and
install the packages.

# Packages list
- libtool
- openssl
- autoconf
- automake
- libevent
- tmux
- tree

# Usage
With your normal user account (no root):

    $ cd macos-packages
    $ make DEST_DIR=~/opt

Using the optional DEST_DIR parameter will instruct Make to install the packages
in this directory, thus the previous command will install packages in ~/opt
directory.
