from setuptools import setup, find_packages
import sys

if sys.version_info.major < 3:
    sys.exit("Error: Please upgrade to Python3")


def get_long_description() -> str:
    with open("README.md") as fp:
        return fp.read()


setup(
    name="py-loop",
    version="0.1.0",
    description="Run commands until it fails",
    long_description=get_long_description(),
    url="https://github.com/jeremad/looper",
    author="Kontrol SAS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=[
        "cli-ui",
    ],
    extras_require={
        "dev": [
            "flake8",
            "mypy",
            "pytest",
        ],
    },
    entry_points={"console_scripts": ["looper = looper.main:main"]},
)
