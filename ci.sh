#!/usr/bin/env sh
set -x
set -e

dmenv run flake8 .
dmenv run -- mypy --ignore-missing-imports --strict .
dmenv run pytest
