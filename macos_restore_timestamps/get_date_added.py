import json
import subprocess
from pathlib import Path


def get_date_added(reference_dir):
    reference_dir = Path(reference_dir)
    date_dict = {}
    for element in reference_dir.iterdir():
        date_added = subprocess.check_output(["mdls", "-name", "kMDItemDateAdded", element], encoding='utf-8').split()
        if len(date_added) >= 4:
            date = date_added[2]
            date = f"{date[5:7]}:{date[8:10]}:{date[2:4]}"
            time = date_added[3]
            date_dict[str(element)] = {
                "date": date,
                "time": time
            }

    with open("date_added.json", "w") as f:
        json.dump(date_dict, f, indent=3)
