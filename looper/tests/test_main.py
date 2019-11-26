import looper.main

import pytest


def test_version():
    assert looper.main.main(["--version"]) is None


def test_no_cmd():
    with pytest.raises(SystemExit) as e:
        looper.main.main([""])
    assert e.value.code == 1


def test_cmd():
    assert looper.main.main(["ls", "--max-tries", "1"]) is None
    assert looper.main.main(["--max-tries", "1", "ls"]) is None
