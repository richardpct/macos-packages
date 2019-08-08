.DEFAULT_GOAL := help
AWK           := /usr/bin/awk
DEST_DIR      ?= $(HOME)/test
GO            ?= $(HOME)/opt/go/bin/go
GO_BIN        ?= $(HOME)/go/bin
REPO          ?= github.com/richardpct
GO_SRC        := $(HOME)/go/src/$(REPO)
PACKAGES      := tree \
                 make \
                 htop \
                 tmux \
                 libevent \
                 libtool \
                 openssl \
                 automake \
                 autoconf
VPATH         := $(DEST_DIR)/bin $(foreach pkg,$(PACKAGES),$(GO_SRC)/macos-$(pkg))
vpath %.a $(DEST_DIR)/lib

# If default GO does not exist then looks for in PATH variable
ifeq "$(wildcard $(GO))" ""
  GO_FOUND := $(shell which go)
  GO = $(if $(GO_FOUND),$(GO_FOUND),$(error go is not found))
endif

# $(call install-package,package_name)
define install-package
  $(GO) get -u $(REPO)/macos-$1
  $(GO_BIN)/macos-$1 -destdir=$(DEST_DIR)
endef

.PHONY: help
help: ## Show help
	@echo "Usage: make [DEST_DIR=/tmp] TARGET\n"
	@echo "Targets:"
	@$(AWK) -F ":.* ##" '/.*:.*##/{ printf "%-13s%s\n", $$1, $$2 }' \
	$(MAKEFILE_LIST) \
	| grep -v AWK

.PHONY: all
all: $(PACKAGES) ## Build all packages

.PHONY: update_repo
update_repo: ## Update all repositories
	for pkg in $(PACKAGES); do \
	  $(GO) get -d $(REPO)/macos-$$pkg; \
	done

$(foreach pkg,$(PACKAGES),$(pkg).go): update_repo

tree: tree.go ## Build tree
	$(call install-package,$@)

make: make.go ## Build make
	$(call install-package,$@)

htop: htop.go ## Build htop
	$(call install-package,$@)

tmux: tmux.go libevent.a ## Build tmux
	$(call install-package,$@)

.PHONY: libevent
libevent: libevent.a ## Build libevent

libevent.a: libevent.go glibtool openssl automake
	$(call install-package,libevent)

.PHONY: libtool
libtool: glibtool ## Build libtool

glibtool: libtool.go
	$(call install-package,libtool)

openssl: openssl.go ## Build openssl
	$(call install-package,$@)

automake: automake.go autoconf ## Build automake
	$(call install-package,$@)

autoconf: autoconf.go ## Build autoconf
	$(call install-package,$@)
