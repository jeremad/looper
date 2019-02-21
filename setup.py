from setuptools import setup, find_packages


def get_long_description() -> str:
    with open("README.md") as fp:
        return fp.read()


setup(
    name="py-loop",
    version="0.1.4",
    description="Run commands until it fails",
    long_description=get_long_description(),
    python_requires='>=3.6',
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
