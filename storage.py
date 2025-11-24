# Furkan Ciloglu  |  231ADB104
# Functions for saving valid flights and error records.

from pathlib import Path
from typing import List, Dict, Any
import json


def save_valid_flights(flights: List[Dict[str, Any]], output_path: Path) -> None:
    # Save valid flights to a JSON file as an array of objects.
    data = []

    for flight in flights:
        data.append(
            {
                "flight_id": flight["flight_id"],
                "origin": flight["origin"],
                "destination": flight["destination"],
                "departure_datetime": flight["departure_datetime"],
                "arrival_datetime": flight["arrival_datetime"],
                "price": flight["price"],
            }
        )

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def save_error_records(errors: List[Dict[str, Any]], output_path: Path) -> None:
    # Save error records to a text file.
    # Sort errors by file name and line number to keep output stable.
    sorted_errors = sorted(
        errors,
        key=lambda e: (e.get("file", ""), e.get("line_number", 0)),
    )

    with output_path.open("w", encoding="utf-8") as f:
        for error in sorted_errors:
            line_number = error.get("line_number", 0)
            raw = error.get("raw", "")
            messages = error.get("messages", [])
            reason = ", ".join(messages)

            f.write(f"Line {line_number}: {raw} \u2192 {reason}\n")

def save_query_response(data: List[Dict[str, Any]], filename: Path) -> None:
    # Save query results to a JSON file.
    with filename.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)