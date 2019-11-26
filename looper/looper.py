import subprocess
import time

import cli_ui as ui
import pkg_resources
from typing import Any, List


class InvalidCommand(Exception):
    pass


class Looper:
    def __init__(
        self,
        *,
        cmd: List[str],
        max_tries: int,
        stop_on_first_fail: bool,
        capture: bool,
        delay: float,
        total_time: float,
    ):
        if not cmd or not cmd[0]:
            raise InvalidCommand("no command provided")
        self.cmd = cmd
        self.cmd_str = " ".join(self.cmd)
        self.max_tries = max_tries
        self.stop_on_first_fail = stop_on_first_fail
        self.capture = capture
        self.runs = 0
        self.fails = 0
        self.delay = delay
        self.total_time = total_time
        self.start = 0.0
        self.duration = 0.0
        self.run_durations: List[float] = list()

    def run_cmd(self, **kwargs: Any) -> int:
        run_start_time = time.time()
        ui.info_2(f"run #{self.runs + 1}")
        ui.info_2(self.cmd_str)
        if self.capture:
            kwargs["stdout"] = subprocess.PIPE
            kwargs["stderr"] = subprocess.PIPE
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
        end = time.time()
        self.duration = end - self.start
        self.run_durations.append(end - run_start_time)
        return process.returncode

    def _print_summary(self) -> None:
        summary = (
            f'command "{self.cmd_str}" failed {self.fails} times after {self.runs} '
            + f"tries in {self.duration:.2f} seconds"
        )
        if self.run_durations:
            max_time = max(self.run_durations)
            min_time = min(self.run_durations)
            mean_time = sum(self.run_durations) / len(self.run_durations)
            summary = f"{summary} max: {max_time:.2f}, min: {min_time:.2f}, mean: {mean_time:.2f}"
        ui.info_1(summary)

    def loop(self) -> None:
        self.start = time.time()
        try:
            while True:
                if self.run_cmd():
                    if self.stop_on_first_fail:
                        break
                if self.max_tries and self.runs >= self.max_tries:
                    break
                if self.total_time:
                    ui.info_3(f"time elapsed: {self.duration:.2f} seconds")
                    if self.duration > self.total_time:
                        break
                if self.delay:
                    ui.info_3(f"waiting for {self.delay:.2f} seconds")
                    time.sleep(self.delay)
        except KeyboardInterrupt:
            ui.info_2("Interrupted by user")
        finally:
            self._print_summary()

    @classmethod
    def version(cls) -> str:
        return pkg_resources.require("py-loop")[0].version
