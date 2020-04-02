#!/usr/bin/env sh
set -x
set -e

poetry build
python3 -m twine upload dist/* --verbose
