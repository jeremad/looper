import argparse
import subprocess
import sys

import cli_ui as ui
from typing import List, Optional

ArgsList = Optional[List[str]]

def run(cmd: str, capture: bool) -> int:
    ui.info_2(cmd)
    cmd = cmd.split()
    kwargs = {}
    if capture:
        kwargs['stdout'] = subprocess.PIPE
        kwargs['stderr'] = subprocess.PIPE
    process = subprocess.run(cmd, **kwargs)
    if process.returncode:
        if process.stdout:
            ui.info_1(process.stdout.decode("utf-8"))
        if process.stderr:
            ui.error(process.stderr.decode("utf-8"))
    return process.returncode


def loop(cmd: List, max_tries: int, stop_on_first_fail: bool, capture: bool) -> None:
    if not cmd or not cmd[0]:
        ui.error("no command provided")
        sys.exit(1)
    cmd = cmd[0]
    runs = 0
    fails = 0
    try:
        while True:
            if run(cmd, capture):
                if stop_on_first_fail:
                    return
                fails += 1
            runs += 1
            if max_tries and runs >= max_tries:
                ui.info_1(f"command \"{cmd}\" failed {fails} times after {max_tries} tries")
                return
    except KeyboardInterrupt:
        ui.info_2("Interrupted by user")
        ui.info_1(f"command \"{cmd}\" failed {fails} times after {max_tries} tries")


def main(args: ArgsList = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd", nargs=1, type=str,
        help="The command you want to run in a loop, between double quotes")
    parser.add_argument(
        "-m", "--max-tries", type=int, default=100,
        help="Maximum number of time running the command, 0 means no limit")
    parser.add_argument(
        "-s", "--stop-on-first-fail", action="store_true",
        help="If set looper will stop on the first fail")
    parser.add_argument(
        "-c", "--no-capture", action="store_true",
        help="Don't capture output")
    args_ns = parser.parse_args(args=args)
    loop(args_ns.cmd, args_ns.max_tries, args_ns.stop_on_first_fail, not args_ns.no_capture)
