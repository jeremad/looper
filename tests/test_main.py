import py_loop.main as looper_main

import pytest


def test_version():
    assert looper_main.main(["--version"]) is None


def test_no_cmd():
    with pytest.raises(SystemExit) as e:
        looper_main.main([""])
    assert e.value.code == 1


def test_cmd():
    assert looper_main.main(["ls", "--max-tries", "1"]) is None
    assert looper_main.main(["--max-tries", "1", "ls"]) is None
