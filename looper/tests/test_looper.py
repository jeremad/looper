import re
import pytest

import looper


@pytest.mark.parametrize("max_tries", [1, 10, 100])
def test_max_success(max_tries: int) -> None:
    cmd_looper = looper.Looper(
        cmd=["ls"],
        max_tries=max_tries,
        stop_on_first_fail=False,
        capture=False,
        delay=0,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == max_tries
    assert cmd_looper.fails == 0


@pytest.mark.parametrize("max_tries", [1, 10, 100])
def test_max_fails(max_tries: int) -> None:
    cmd_looper = looper.Looper(
        cmd=["ls", "/plop"],
        max_tries=max_tries,
        stop_on_first_fail=False,
        capture=False,
        delay=0,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == max_tries
    assert cmd_looper.fails == max_tries


def test_stop_on_first_fail() -> None:
    cmd_looper = looper.Looper(
        cmd=["ls", "/plop"],
        max_tries=10,
        stop_on_first_fail=True,
        capture=False,
        delay=0,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.runs == 1
    assert cmd_looper.fails == 1


def test_fail_and_std() -> None:
    cmd_looper = looper.Looper(
        cmd=["ls", "/plop"],
        max_tries=1,
        stop_on_first_fail=True,
        capture=True,
        delay=0,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.fails == 1


def test_wrong_cmd() -> None:
    cmd_looper = looper.Looper(
        cmd=["llllll"],
        max_tries=10,
        stop_on_first_fail=True,
        capture=False,
        delay=0,
        total_time=0,
    )
    with pytest.raises(looper.InvalidCommand):
        cmd_looper.loop()
    assert cmd_looper.runs == 0
    assert cmd_looper.fails == 0


def test_empty_cmd() -> None:
    with pytest.raises(looper.InvalidCommand):
        looper.Looper(
            cmd=[""],
            max_tries=10,
            stop_on_first_fail=True,
            capture=False,
            delay=0,
            total_time=0,
        )


def test_stop_after_a_while() -> None:
    cmd_looper = looper.Looper(
        cmd=[
            "python",
            "-c",
            "import time; import sys; sys.exit(not int(time.time() % 3))",
        ],
        max_tries=10000000000,
        stop_on_first_fail=True,
        capture=False,
        delay=0,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.fails == 1


def test_total_delay() -> None:
    max_tries = 10
    delay = 0.1
    cmd_looper = looper.Looper(
        cmd=["ls"],
        max_tries=max_tries,
        stop_on_first_fail=True,
        capture=False,
        delay=delay,
        total_time=0,
    )
    cmd_looper.loop()
    assert cmd_looper.fails == 0
    assert cmd_looper.runs == max_tries
    diff = cmd_looper.duration - (max_tries - 1) * delay
    assert diff > 0
    assert diff < 0.1


def test_total_time() -> None:
    total_time = 1
    max_tries = 100
    delay = 0.1
    cmd_looper = looper.Looper(
        cmd=["ls"],
        max_tries=max_tries,
        stop_on_first_fail=True,
        capture=False,
        delay=delay,
        total_time=total_time,
    )
    cmd_looper.loop()
    assert cmd_looper.fails == 0
    assert cmd_looper.runs <= (total_time / delay + 1)
    diff = cmd_looper.duration - total_time
    assert diff > 0
    assert cmd_looper.duration - total_time < 0.1


def test_version() -> None:
    pattern = re.compile(r"\d+\.\d+\.\d+")
    version = looper.Looper.version()
    assert pattern.match(version)
