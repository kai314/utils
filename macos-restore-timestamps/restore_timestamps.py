#!/usr/bin/sudo python3

import json
import logging
import os
import shutil
import subprocess
from pathlib import Path
from typing import Union

"""
Script for applying date added from a copy of the files in another directory (or volume).
Make sure to run as sudo (required for changing system date / time).
"""


def transfer_timestamps(target_dir: Union[str, Path], reference_dir: Union[str, Path], json_file: str) -> None:
    reference_dir = Path(reference_dir)
    target_dir = Path(target_dir)
    print(f"Editing dates in directory {target_dir}")
    temp_dir = os.environ.get("TMPDIR") or "/var/folders/jr/td9rb8x92llg9mmgn92sw8ch0000gn/T"
    with open(json_file, "r") as f:
        date_dict = json.load(f)
    print(f"loaded dict with {len(date_dict)} entries")

    subprocess.check_call(["systemsetup", "-setusingnetworktime", "Off"])
    # iterate through all items in directory (only top level)
    for item in target_dir.iterdir():
        # get date added from equivalent item in source dir
        entry = date_dict.get(reference_dir / item.name)
        if entry:
            date = entry["date"]
            time = entry["time"]

            # set system date + time
            subprocess.check_call(["systemsetup", "-setdate", date])
            subprocess.check_call(["systemsetup", "-settime", time])
            # move item to temp directory
            temp_path = shutil.move(str(item), temp_dir)
            # move item back
            shutil.move(temp_path, str(item))
            print(f"edited {item}")
        else:
            print(f"Could not find metadata for file {item}")

    # restore system date + time
    subprocess.check_call(["systemsetup", "-setusingnetworktime", "On"])
