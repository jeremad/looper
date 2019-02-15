import subprocess

import cli_ui as ui
import pkg_resources
from typing import Any, List


class InvalidCommand(Exception):
    pass


class Looper:
    def __init__(self, cmd_str: str, max_tries: int, stop_on_first_fail: bool, capture: bool):
        if not cmd_str:
            raise InvalidCommand("no command provided")
        self.cmd_str = cmd_str
        self.cmd = self._split()
        self.max_tries = max_tries
        self.stop_on_first_fail = stop_on_first_fail
        self.capture = capture
        self.runs = 0
        self.fails = 0

    def _split(self) -> List[str]:
        cmd_list = self.cmd_str.split()
        res = list()
        tmp = ""
        for arg in cmd_list:
            if arg.startswith("'") and not arg.endswith("'"):
                tmp = arg.strip("'")
            elif arg.endswith("'") and not arg.startswith("'"):
                tmp += " "
                tmp += arg.strip("'")
                res.append(tmp)
                tmp = ""
            elif tmp:
                tmp += f" {arg}"
            else:
                res.append(arg)
        return res

    def run_cmd(self, **kwargs: Any) -> int:
        ui.info_2(self.cmd_str)
        if self.capture:
            kwargs['stdout'] = subprocess.PIPE
            kwargs['stderr'] = subprocess.PIPE
        try:
            process = subprocess.run(self.cmd, **kwargs)
        except FileNotFoundError:
            raise InvalidCommand(f"unkown command provided: {self.cmd[0]}")
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

    @classmethod
    def version(cls) -> str:
        return pkg_resources.require("py-loop")[0].version
