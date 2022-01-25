import py_loop.main as looper_main

import pytest


def test_version() -> None:
    looper_main.main(["--version"])


def test_no_cmd() -> None:
    with pytest.raises(SystemExit) as e:
        looper_main.main([""])
    assert e.value.code == 1


def test_cmd() -> None:
    looper_main.main(["ls", "--max-tries", "1"])
    looper_main.main(["--max-tries", "1", "ls"])
