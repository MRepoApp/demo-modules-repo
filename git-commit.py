#!/usr/bin/env python3

import json
import subprocess
from argparse import ArgumentParser
from datetime import datetime, UTC
from pathlib import Path

MODULES_JSON = "modules.json"
JSON_DIR = "json"


class Main:
    @classmethod
    def generate_parser(cls) -> ArgumentParser:
        cwd_folder = Path(__name__).resolve().parent

        parser = ArgumentParser()
        parser.add_argument(
            "-D",
            "--directory",
            dest="working_dir",
            metavar="DIR",
            type=str,
            default=cwd_folder.as_posix(),
            help="set working directory"
        )

        return parser

    @classmethod
    def commit(cls, msg: str, cwd_dir: Path):
        subprocess.run(
            args=["git", "commit", "-m", msg],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=cwd_dir
        )

    @classmethod
    def exec(cls):
        parser = cls.generate_parser()
        args = parser.parse_args()

        working_dir = Path(args.working_dir)
        modules_json = working_dir.joinpath(JSON_DIR, MODULES_JSON)
        if not modules_json.exists():
            return

        with open(modules_json, "r") as f:
            modules = json.load(f)
            timestamp = modules["timestamp"] / 1000
            time = datetime.fromtimestamp(timestamp, UTC)
            msg = f"Update by CLI ({time})"
            cls.commit(msg, working_dir)


if __name__ == "__main__":
    Main.exec()
