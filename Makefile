SHELL :=/bin/bash
CWD := $(PWD)
TMP_PATH := $(CWD)/.tmp
VENV_PATH := $(CWD)/.venv

.PHONY: test clean

clean:
	@rm -rf $(TMP_PATH) __pycache__ .pytest_cache
	@find . -name '*.pyc' -delete

venv:
	@virtualenv -p python3 $(VENV_PATH)

setup:
	@pip3 install -U -e .[dev]

venv_test:
	@pytest -vvv

build:
	@docker build --no-cache --target=test -t leaderboard:test .
	@docker build --no-cache --target=main -t leaderboard .

format:
	@black .

check:
	@black --check --diff .
	@pyright --verbose

run:
	@./run-local.sh
