#!/usr/bin/make

.DEFAULT_GOAL = all
SHELL := bash

# Build parameters
VERSION = v0.0.1
SEMVERSION = $(subst v,,$(VERSION))

# Sources
KLE_COLOURISER_RAW_SRCS = src/kle_colouriser.py $(filter-out src/kle_colouriser/version.py,$(wildcard src/kle_colouriser/*.py))
KLE_COLOURISER_RUN_SRCS = src/kle_colouriser/version.py $(KLE_COLOURISER_RAW_SRCS)
KLE_COLOURISER_DATA_SRCS = $(wildcard keebs/*) $(wildcard kits/*) $(wildcard themes/*)
KLE_COLOURISER_DIST_SRCS = requirements.txt README.md LICENSE kle-colouriser.pdf kle-colouriser.1.gz ChangeLog $(KLE_COLOURISER_RUN_SRCS) $(KLE_COLOURISER_DATA_SRCS)
DIST_PKG_SRCS = kle-colouriser LICENSE kle-colouriser.pdf kle-colouriser.1.gz ChangeLog
SDIST_PKG_SRCS = LICENSE kle-colouriser.pdf kle-colouriser.1.gz ChangeLog build-binary.sh $(KLE_COLOURISER_RUN_SRCS)

# Distributables
DISTRIBUTABLES = kle-colouriser kle-colouriser.zip

# Programs
ZIP = zip -q -MM
XZ = xz
XZ_FLAGS = -kf

all: kle-colouriser
.PHONY: all

run: $(KLE_COLOURISER_RUN_SRCS)
	-@python3 ./kle_colouriser.py -v3
.PHONY: run

github-dist: dist zip-dist
.PHONY: github-dist

dist: $(DISTRIBUTABLES)
.PHONY: dist

zip-dist: kle-colouriser.zip
.PHONY: dist

build-binary.sh: build-binary.sh.in
	sed 's/KLE_COLOURISER_RUN_SRCS/$(subst /,\/,$(KLE_COLOURISER_RUN_SRCS))/g'  < $< > $@
	chmod 755 $@

kle-colouriser.zip: $(KLE_COLOURISER_DIST_SRCS)
	$(ZIP) $@ $^

kle-colouriser-$(SEMVERSION).tar.xz: keycov-$(SEMVERSION).tar
	$(XZ) $(XZ_FLAGS) $<

kle-colouriser-bin-$(SEMVERSION).tar.xz: keycov-bin-$(SEMVERSION).tar
	$(XZ) $(XZ_FLAGS) $<

kle-colouriser-$(SEMVERSION).tar: $(SDIST_PKG_SRCS)
	[[ ! -d $(subst .tar,,$@) ]] && mkdir $(subst .tar,,$@)/ || true
	cp --parents $^ $(subst .tar,,$@)/
	tar -cf $@ $(foreach f,$^,$(subst .tar,,$@)/$f)

kle-colouriser-bin-$(SEMVERSION).tar: $(DIST_PKG_SRCS)
	[[ ! -d $(subst .tar,,$@) ]] && mkdir $(subst .tar,,$@)/ || true
	cp --parents $^ $(subst .tar,,$@)/
	tar -cf $@ $(foreach f,$^,$(subst .tar,,$@)/$f)

kle-colouriser: $(KLE_COLOURISER_RUN_SRCS)
	[[ ! -d kle-colouriser-binary/ ]] && mkdir kle-colouriser-binary/ || true
	[[ ! -d kle-colouriser-binary/kle_colouriser/ ]] && mkdir kle-colouriser-binary/kle_colouriser/ || true
	cp --parents $(KLE_COLOURISER_RUN_SRCS) kle-colouriser-binary/
	cp kle-colouriser-binary/src/kle_colouriser.py kle-colouriser-binary/src/__main__.py
	(cd kle-colouriser-binary/src/ && zip -q -MM - $$(find)) > $@-binarytemp
	(echo '#!/usr/bin/env python3' | cat - $@-binarytemp) > $@
	chmod 700 $@

kle-colouriser.pdf: kle-colouriser.1
	groff -man -Tpdf -fH < $< > $@

kle-colouriser.1.gz: kle-colouriser.1
	gzip -kf $<

kle-colouriser.1: kle-colouriser src/kle_colouriser/version.py kle-colouriser.yml
	help2man --no-info --no-discard-stderr --name "$$(yq -y .desc kle-colouriser.yml | head -n -1)" $< > $@

src/kle_colouriser/version.py: src/kle_colouriser/version.py.in kle-colouriser.yml
	(sed "s/s_version/$(VERSION)/" | sed "s/s_name/$(shell yq -y .name kle-colouriser.yml | head -n1)/" | sed "s/s_desc/$(shell yq -y .desc kle-colouriser.yml | head -n1)/") < $< > $@

kle-colouriser.yml: kle-colouriser.yml.in
	sed "s/VERSION/$(VERSION)/g" < $< > $@

%.py: ;
%.py.in: ;

requirements.txt: $(KLE_COLOURISER_RAW_SRCS)
	pipreqs --force --print >$@

ChangeLog: scripts/change-log.sh scripts/change-log-format.awk $(KLE_COLOURISER_RUN_SRCS)
	./$< > $@

clean:
	$(RM) -r requirements.txt src/kle_colouriser/version.py kle-colouriser.zip __pycache__/ kle-colouriser kle-colouriser-*.tar kle-colouriser-*.tar.xz kle-colouriser.yml $(wildcard *.1) $(wildcard *.1.gz) kle-colouriser-binary/ kle-colouriser-binarytemp ChangeLog build-binary.sh kle-colouriser.pdf
