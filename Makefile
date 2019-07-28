.DEFAULT_GOAL := all
DEST_DIR      ?= $(HOME)/test
GO            ?= $(HOME)/opt/go/bin/go
GO_BIN        ?= $(HOME)/go/bin
REPO          ?= github.com/richardpct
SRC           := $(HOME)/go/src/$(REPO)
PACKAGES      := libtool \
                 openssl \
                 autoconf \
                 automake \
                 libevent \
                 tmux \
                 tree \
                 make
VPATH         := $(DEST_DIR)/bin $(foreach pkg,$(PACKAGES),$(SRC)/macos-$(pkg))
vpath %.a $(DEST_DIR)/lib

# $(call install-package,package_name)
define install-package
  $(GO) get -u $(REPO)/macos-$1
  $(GO_BIN)/macos-$1 -destdir=$(DEST_DIR)
endef

.PHONY: all
all: $(PACKAGES)

.PHONY: update_repo
update_repo:
	for pkg in $(PACKAGES); do \
	  $(GO) get -d $(REPO)/macos-$$pkg; \
	done

%: update_repo ;

%.go: ;

.PHONY: libtool
libtool: glibtool

glibtool: libtool.go
	$(call install-package,libtool)

openssl: openssl.go
	$(call install-package,$@)

autoconf: autoconf.go
	$(call install-package,$@)

automake: autoconf automake.go
	$(call install-package,$@)

.PHONY: libevent
libevent: libevent.a

libevent.a: automake glibtool openssl libevent.go
	$(call install-package,libevent)

tmux: libevent.a tmux.go
	$(call install-package,$@)

tree: tree.go
	$(call install-package,$@)

make: make.go
	$(call install-package,$@)
