# Furkan Ciloglu  |  231ADB104
# Functions for loading an existing JSON flight database.

import json
from pathlib import Path
from typing import List, Dict, Any


def load_flights_from_json(path: Path) -> List[Dict[str, Any]]:
    # Load existing flights from a JSON database file.
    # The file is expected to contain an array of flight objects.

    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise SystemExit(f"Error: Invalid JSON format in file {path}")

    if not isinstance(data, list):
        raise SystemExit("Error: JSON database must be an array of flight objects")

    return data
