# Furkan Ciloglu  |  231ADB104
# CSV loading functions for flight data.

from pathlib import Path
from typing import List, Dict, Any


def read_csv_file(path: Path) -> List[Dict[str, Any]]:
    # Read a single CSV file line by line.
    # Returns a list of records with file name, line number and raw text.
    records: List[Dict[str, Any]] = []

    with path.open("r", encoding="utf-8") as f:
        for index, line in enumerate(f, start=1):
            records.append(
                {
                    "file": path.name,
                    "line_number": index,
                    "raw": line.rstrip("\n"),
                }
            )

    return records


def read_csv_from_directory(directory: Path) -> List[Dict[str, Any]]:
    # Read all .csv files in a directory.
    # Files are processed in sorted order by name.
    all_records: List[Dict[str, Any]] = []

    for csv_path in sorted(directory.glob("*.csv")):
        if csv_path.is_file():
            all_records.extend(read_csv_file(csv_path))

    return all_records
