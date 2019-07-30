.DEFAULT_GOAL := help
AWK           := /usr/bin/awk
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
                 make \
                 htop
VPATH         := $(DEST_DIR)/bin $(foreach pkg,$(PACKAGES),$(SRC)/macos-$(pkg))
vpath %.a $(DEST_DIR)/lib

# $(call install-package,package_name)
define install-package
  $(GO) get -u $(REPO)/macos-$1
  $(GO_BIN)/macos-$1 -destdir=$(DEST_DIR)
endef

.PHONY: all
all: $(PACKAGES) ## Build all packages

.PHONY: update_repo
update_repo: ## Update all repositories
	for pkg in $(PACKAGES); do \
	  $(GO) get -d $(REPO)/macos-$$pkg; \
	done

$(foreach pkg,$(PACKAGES),$(pkg).go): update_repo

.PHONY: libtool
libtool: glibtool ## Build libtool

glibtool: libtool.go
	$(call install-package,libtool)

openssl: openssl.go ## Build openssl
	$(call install-package,$@)

autoconf: autoconf.go ## Build autoconf
	$(call install-package,$@)

automake: autoconf automake.go ## Build automake
	$(call install-package,$@)

.PHONY: libevent
libevent: libevent.a ## Build libevent

libevent.a: automake glibtool openssl libevent.go
	$(call install-package,libevent)

tmux: libevent.a tmux.go ## Build tmux
	$(call install-package,$@)

tree: tree.go ## Build tree
	$(call install-package,$@)

make: make.go ## Build make
	$(call install-package,$@)

htop: htop.go ## Build htop
	$(call install-package,$@)

.PHONY: help
help:
	@printf "%-15s %s\n\n" "Target" "Description"
	@$(AWK) -F ":.* ##" '/.*:.*##/{ printf "%-15s%s\n", $$1, $$2 }' \
	$(MAKEFILE_LIST) \
	| grep -v AWK
