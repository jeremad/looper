import subprocess
import sys

import cli_ui as ui
from typing import Any


class Looper:

    def __init__(self, cmd_str: str, max_tries: int, stop_on_first_fail: bool, capture: bool):
        self.cmd_str = cmd_str
        self.cmd = cmd_str.split()
        self.max_tries = max_tries
        self.stop_on_first_fail = stop_on_first_fail
        self.capture = capture
        self.runs = 0
        self.fails = 0

    def run_cmd(self, **kwargs: Any) -> int:
        ui.info_2(self.cmd_str)
        if self.capture:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE
        try:
            process = subprocess.run(self.cmd, **kwargs)
        except FileNotFoundError:
            ui.error(f"unkown command provided: {self.cmd[0]}")
            sys.exit(1)
        self.runs += 1
        if process.returncode:
            self.fails += 1
            if process.stdout:
                ui.info_1(process.stdout.decode("utf-8"))
            if process.stderr:
                ui.error(process.stderr.decode("utf-8"))
        return process.returncode

    def _print_summary(self) -> None:
        ui.info_1(f"command \"{self.cmd_str}\" failed {self.fails} times after {self.runs} tries")

    def loop(self) -> None:
        try:
            while True:
                if self.run_cmd():
                    if self.stop_on_first_fail:
                        break
                if self.max_tries and self.runs >= self.max_tries:
                    break
        except KeyboardInterrupt:
            ui.info_2("Interrupted by user")
        finally:
            self._print_summary()
