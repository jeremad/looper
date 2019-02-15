[![License](https://img.shields.io/github/license/jeremad/looper.svg)](https://opensource.org/licenses/MIT)
[![Build](https://img.shields.io/travis/jeremad/looper/master.svg)](https://travis-ci.org/jeremad/looper)

# Basic tool to run commands in loop

This tool was intended to help QA guy like me with flaky tests, buy either measuring the "flakyness" of the test, or run it until it fails to debug it.

## Usage

Let's say your test command is `run test`


### Debug

You want to run a test untils it fails to debug it, and you know it may take a while:
```
$ looper --max-tries 0 --stop-on-first-fail "run test"
```

`max-tries` to 0, means that there is no limit to the number of times a test can sucessfully run

### Measure

You want to approximately the failing rate of a test of out 1000 runs:

```
$ looper --max-tries 1000 "run test"
```

At the end you will have a sumary

## Installation

`pip install --user py-loop`
