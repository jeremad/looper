import re
import pytest

import looper


@pytest.mark.parametrize("max_tries", [1, 10, 100])
def test_max_success(max_tries: int) -> None:
    cmd_looper = looper.Looper(
        cmd_str="ls",
        max_tries=max_tries,
        stop_on_first_fail=False,
        capture=False,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == max_tries
    assert cmd_looper.fails == 0


@pytest.mark.parametrize("max_tries", [1, 10, 100])
def test_max_fails(max_tries: int) -> None:
    cmd_looper = looper.Looper(
        cmd_str="ls /plop",
        max_tries=max_tries,
        stop_on_first_fail=False,
        capture=False,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == max_tries
    assert cmd_looper.fails == max_tries


def test_stop_on_first_fail() -> None:
    cmd_looper = looper.Looper(
        cmd_str="ls /plop",
        max_tries=10,
        stop_on_first_fail=True,
        capture=False,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == 1
    assert cmd_looper.fails == 1


def test_wrong_cmd() -> None:
    cmd_looper = looper.Looper(
        cmd_str="llllll",
        max_tries=10,
        stop_on_first_fail=True,
        capture=False,
    )
    with pytest.raises(looper.InvalidCommand):
        cmd_looper.loop()
    assert cmd_looper.runs == 0
    assert cmd_looper.fails == 0


def test_empty_cmd() -> None:
    cmd_looper = looper.Looper(
        cmd_str="llllll",
        max_tries=10,
        stop_on_first_fail=True,
        capture=False,
    )
    with pytest.raises(looper.InvalidCommand):
        cmd_looper.loop()
    assert cmd_looper.runs == 0
    assert cmd_looper.fails == 0


def test_stop_after_a_while() -> None:
    cmd_looper = looper.Looper(
        cmd_str="python -c 'import time; import sys; sys.exit(not int(time.time() % 3))'",
        max_tries=10000000000,
        stop_on_first_fail=True,
        capture=False,
    )
    cmd_looper.loop()
    assert cmd_looper.fails == 1

def test_version() -> None:
    pattern = re.compile(r"\d+\.\d+\.\d+")
    version = looper.Looper.version()
    assert pattern.match(version)
