from setuptools import setup, find_packages


def get_long_description() -> str:
    with open("README.md") as fp:
        return fp.read()


setup(
    name="py-loop",
    version="0.3.1",
    description="Run commands until it fails",
    long_description=get_long_description(),
    python_requires='>=3.6',
    url="https://github.com/jeremad/looper",
    author="Kontrol SAS",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    install_requires=[
        "cli-ui",
    ],
    extras_require={
        "dev": [
            "black",
            "codacy-coverage",
            "codecov",
            "flake8",
            "mypy",
            "pytest",
            "pytest-cov",
        ],
    },
    entry_points={"console_scripts": ["looper = looper.main:main"]},
)
