import argparse
import sys

import cli_ui as ui
from typing import List, Optional

from looper.looper import Looper

ArgsList = Optional[List[str]]


def main(args: ArgsList = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd", nargs='?', type=str, default="",
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
    parser.add_argument(
        "-v", "--version", action="store_true")
    args_ns = parser.parse_args(args=args)
    if args_ns.version:
        ui.info_1(Looper.version())
        return
    if not args_ns.cmd or not args_ns.cmd[0]:
        ui.error("no command provided")
        sys.exit(1)
    looper = Looper(
        args_ns.cmd,
        args_ns.max_tries,
        args_ns.stop_on_first_fail,
        not args_ns.no_capture,
        )
    looper.loop()
