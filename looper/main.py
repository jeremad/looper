import argparse
import sys

import cli_ui as ui
from typing import List, Optional

from looper.looper import Looper

ArgsList = Optional[List[str]]


def main(args: ArgsList = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "cmd",
        nargs=argparse.REMAINDER,
        help="The command you want to run in a loop (at the end of the full command line)",
    )
    parser.add_argument(
        "-m",
        "--max-tries",
        type=int,
        default=100,
        help="Maximum number of time running the command, 0 means no limit",
    )
    parser.add_argument(
        "-s",
        "--stop-on-first-fail",
        action="store_true",
        help="If set looper will stop on the first fail",
    )
    parser.add_argument(
        "-c", "--no-capture", action="store_true", help="Don't capture output"
    )
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument(
        "-d", "--delay", type=float, default=0, help="Delay between runs"
    )
    parser.add_argument(
        "-t",
        "--total-time",
        type=float,
        default=0,
        help="Total time of the runs in seconds, O means no limit",
    )
    args_ns = parser.parse_args(args=args)
    if args_ns.version:
        ui.info_1(Looper.version())
        return
    if not args_ns.cmd or not args_ns.cmd[0]:
        ui.error("no command provided")
        sys.exit(1)
    looper = Looper(
        cmd=args_ns.cmd,
        max_tries=args_ns.max_tries,
        stop_on_first_fail=args_ns.stop_on_first_fail,
        capture=(not args_ns.no_capture),
        delay=args_ns.delay,
        total_time=args_ns.total_time,
    )
    looper.loop()
