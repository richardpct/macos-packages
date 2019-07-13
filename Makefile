.PHONY: all

.DEFAULT_GOAL := all
# DEST_DIR is the directory where the packages will be installed
DEST_DIR      ?= $(HOME)/test
GOPATH        ?= $(HOME)/go
VPATH         := $(DEST_DIR)/bin
GO_EXISTS     := $(shell which go)
vpath %.a $(DEST_DIR)/lib

ifndef GO_EXISTS
  $(error go compiler is not found)
endif

# $(call install-package,package_name)
define install-package
  go get -u github.com/richardpct/macos-$1
  $(GOPATH)/bin/macos-$1 -destdir=$(DEST_DIR)
endef

all: glibtool openssl autoconf automake libevent.a tmux tree make

glibtool:
ifeq "$(wildcard $(DEST_DIR))" ""
	@mkdir $(DEST_DIR)
endif
	$(call install-package,libtool)

openssl:
	$(call install-package,$@)

autoconf:
	$(call install-package,$@)

automake: autoconf
	$(call install-package,$@)

libevent.a: automake glibtool openssl
	$(call install-package,libevent)

tmux: libevent.a
	$(call install-package,$@)

tree:
	$(call install-package,$@)

make:
	$(call install-package,$@)
