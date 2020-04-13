.DEFAULT_GOAL  := help
DEST_DIR       ?= /tmp/test
GO             ?= $(HOME)/opt/go/bin/go
GO_BIN         ?= $(HOME)/go/bin
REPO           ?= github.com/richardpct
GO_SRC         := $(HOME)/go/src/$(REPO)
CLAMAV_DB_DIR  := $(DEST_DIR)/var/lib/clamav
FRESHCLAM_CONF := $(DEST_DIR)/etc/clamav/freshclam.conf
PACKAGES       := tree \
                  make \
                  htop \
                  tmux \
                  clamav \
                  libevent \
                  libtool \
                  openssl \
                  automake \
                  autoconf \
                  pcre2
VPATH          := $(DEST_DIR)/bin $(foreach pkg,$(PACKAGES),$(GO_SRC)/macos-$(pkg))
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
	@awk -F ":.* ##" '/.*:.*##/{ printf "%-13s%s\n", $$1, $$2 }' \
	$(MAKEFILE_LIST) \
	| grep -v awk

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

.PHONY: clamav
clamav: clamscan  ## Build clamav

clamscan: clamav.go $(CLAMAV_DB_DIR) openssl pcre2-config
	$(call install-package,clamav)
	@cp $(FRESHCLAM_CONF).sample $(FRESHCLAM_CONF)
	@sed -i -e "s/^\(Example\)$$/#\1/" $(FRESHCLAM_CONF)

$(CLAMAV_DB_DIR):
	@mkdir -p $@

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

.PHONY: pcre2
pcre2: pcre2-config ## Build pcre2

pcre2-config: pcre2.go
	$(call install-package,pcre2)
