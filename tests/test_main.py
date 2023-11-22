import pytest

import py_loop.main as looper_main


def test_version() -> None:
    looper_main.main(["--version"])


def test_no_cmd() -> None:
    with pytest.raises(SystemExit) as e:
        looper_main.main([""])
    assert e.value.code == 1


def test_parsing() -> None:
    looper = looper_main.main(["--max-tries", "7", "ls"])
    assert looper is not None
    assert looper.max_tries == 7
