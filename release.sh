#!/usr/bin/env sh
set -x
set -e

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/* --verbose
