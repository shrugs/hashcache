SHELL=/bin/bash

pull-vocab:
	@python pull-vocab.py

gen-vocab:
	pandoc -s -i -t revealjs \
		--variable transition="none" \
		-o vocab.html \
		vocab.md

open-vocab:
	@open vocab.html

all: pull-vocab gen-vocab open-vocab
