#!/usr/bin/env sh
set -x
set -e

poetry build
poetry run twine upload dist/* --verbose
