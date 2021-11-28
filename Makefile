PYTHON ?= python3

.PHONY: all
all:
	

.PHONY: help
help:
	@echo "Makefile for FAI Python Lib"
	@echo "==========================="
	@echo "Supported make targets:"
	@echo "* all: does nothing"
	@echo "* help: show this help"
	@echo "* format: format code"
	@echo "* test: run unittests"
	@echo "* check: run tests and additional checks"
	@echo "* build: build python package"
	@echo "* doc: build documentation"
	@echo "* clean: remove build artefacts"

.PHONY: format
format:
	$(PYTHON) -m yapf --recursive --in-place .

.PHONY: test
test:
	$(PYTHON) -m pytest
	$(MAKE) -C docs doctest

.PHONY: check
check: test
	$(PYTHON) -m yapf --recursive --diff .
	$(PYTHON) -m pylint fai

.PHONY: build
build:
	$(PYTHON) -m build

.PHONY: doc
doc:
	$(MAKE) -C docs html

.PHONY: clean
clean:
	rm -rf fai.egg-info/ build/ dist/ fai/_version.py
