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
- pcre2
- tmux
- clamav
- tree
- make
- htop

# Usage
All the following commands should be performed with your normal user account
(no root).

To display all commands available:

    $ make

or

    $ make help

To install all packages:

    $ cd macos-packages
    $ make DEST_DIR=~/opt all

Using the optional DEST_DIR parameter will instruct Make to install the packages
in this directory, thus the previous command will install the packages in ~/opt
directory.
