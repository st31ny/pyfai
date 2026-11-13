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
	@echo "* pipenv: sync dependencies to the pipenv (requires root)"
	@echo "* format: format code"
	@echo "* test: run unittests"
	@echo "* pylint: run pylint"
	@echo "* check_coverage: test coverage percentage"
	@echo "* check_format: test source code formatting"
	@echo "* check_pylint: assert pylint score is high enough"
	@echo "* build: build python package"
	@echo "* doc: build documentation"
	@echo "* clean: remove build artefacts"

export PIPENV_VENV_IN_PROJECT = 1
PIPENV                 := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))/.venv

.PHONY: pipenv
pipenv: $(PIPENV)/Pipfile.lock

$(PIPENV)/Pipfile.lock: Pipfile.lock
	pipenv --python /usr/bin/python3 install --deploy --dev --ignore-pipfile
	pipenv clean
	cp $< $@

.PHONY: format
format: pipenv
	pipenv run yapf --recursive --in-place fai tests docs system

.PHONY: check_format
check_format: pipenv
	pipenv run yapf --recursive --diff fai tests docs system

.PHONY: test
test: pipenv
	mkdir -p ./build/
	@$(eval LOGFILE := $(shell mktemp --tmpdir faitest.XXXXXX))
	pipenv run pytest --log-file=$(LOGFILE) --junitxml=./build/junit.xml \
		--cov --cov-context=test --cov-fail-under 0 --cov-report term --cov-report=xml:build/coverage/coverage.xml --cov-report=html:build/coverage ;
	$(MAKE) -C docs doctest
	@if test -s $(LOGFILE); then echo "ERROR: stdout/stderr output detected:\n----------------" ; cat $(LOGFILE) ; echo "================" ; rm -f $(LOGFILE) ; exit 2 ; fi
	@rm -f $(LOGFILE)

.PHONY: check_coverage
check_coverage: pipenv
	pipenv run coverage report

.PHONY: pylint
pylint: pipenv
	mkdir -p ./build/pylint
	pipenv run pylint --exit-zero -j0 --output-format=json:./build/pylint/pylint.json,json2:./build/pylint/pylint2.json,text:./build/pylint/pylint.log,colorized fai
	pipenv run pylint-json2html -o ./build/pylint/index.html ./build/pylint/pylint.json
	@PYLINT_SCORE=$$(python3 -c "import json; print(json.load(open('./build/pylint/pylint2.json', 'rb'))['statistics']['score'])"); \
	pipenv run anybadge --label=pylint --file=build/pylint/pylint.svg --value=$$PYLINT_SCORE --value-format "%.2f" -o 9=red 9.5=yellow 10=green

.PHONY: check_pylint
check_pylint:
	@python3 -c "import json; import tomllib; \
		CFG = tomllib.load(open('pyproject.toml', 'rb'))['tool']['pylint']['main']; \
		PL = json.load(open('./build/pylint/pylint2.json', 'rb')); \
		score = PL['statistics']['score']; \
		SCORE = CFG['fail-under']; \
		assert score >= SCORE, f'Score too low: {score} (required: {SCORE})'; \
		FORBIDDEN=((set(x['symbol'] for x in PL['messages']) | set(x['messageId'] for x in PL['messages'])) & set(CFG.get('fail-on', []))); \
		assert not FORBIDDEN, f'Forbidden messages: {FORBIDDEN}'; \
		"

.PHONY: check
check:
	$(MAKE) check_format
	$(MAKE) check_coverage
	$(MAKE) check_pylint

.PHONY: build
build:
	$(PYTHON) -m build

.PHONY: doc
doc: pipenv
	$(MAKE) -C docs html

.PHONY: clean
clean:
	rm -rf fai.egg-info/ build/ dist/ fai/_version.py
