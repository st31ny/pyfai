.PHONY: all
all:
	

.PHONY: help
help:
	@echo "Makefile for FAI Python Lib"
	@echo "==========================="
	@echo "Supported make targets:"
	@echo "* all: does nothing"
	@echo "* help: show this help"
	@echo "* test: run unittests"
	@echo "* build: build python package"
	@echo "* clean: remove build artefacts"

.PHONY: test
test:
	python3 -m pytest

.PHONY: build
build:
	python3 -m build

.PHONY: clean
clean:
	rm -rf fai.egg-info/ build/ dist/ fai/_version.py
