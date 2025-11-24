# Furkan Ciloglu  |  231ADB104
# Validation functions for flight records.

from datetime import datetime
from typing import List, Dict, Any, Tuple
import re

# Small set of known airport codes used in the sample data.
# This is enough for the assignment and for basic validation.
KNOWN_AIRPORT_CODES = {
    "LHR", "JFK", "FRA", "RIX", "OSL", "HEL",
    "CDG", "DXB", "DOH", "SYD", "AMS", "BRU",
    "LAX", "ARN",
}


def is_header_line(text: str) -> bool:
    # Check if the line looks like the CSV header.
    return text.lower().startswith(
        "flight_id,origin,destination,departure_datetime,arrival_datetime,price"
    )


def validate_flight_id(value: str, messages: List[str]) -> None:
    # Flight ID must be 2-8 alphanumeric characters.
    if len(value) > 8:
        messages.append("flight_id too long (more than 8 characters)")
        return
    if len(value) < 2:
        messages.append("flight_id too short (less than 2 characters)")
        return
    if not re.fullmatch(r"[A-Za-z0-9]+", value):
        messages.append("flight_id contains invalid characters")


def validate_airport_code(value: str, field_name: str, messages: List[str]) -> None:
    # Airport code must be present and follow the correct format.
    if not value:
        messages.append(f"missing {field_name} field")
        return

    if not re.fullmatch(r"[A-Z]{3}", value):
        messages.append(f"invalid {field_name} code")
        return

    if value not in KNOWN_AIRPORT_CODES:
        messages.append(f"invalid {field_name} code")



def parse_datetime(value: str, field_name: str, messages: List[str]):
    # Try to parse a datetime in the expected format.
    try:
        return datetime.strptime(value, "%Y-%m-%d %H:%M")
    except ValueError:
        messages.append(f"invalid {field_name} datetime")
        return None


def validate_price(value: str, messages: List[str]):
    # Price must be a positive float.
    try:
        price = float(value)
    except ValueError:
        messages.append("invalid price value")
        return None

    if price < 0:
        messages.append("negative price value")
        return None
    if price == 0:
        messages.append("price must be positive")
        return None

    return price


def validate_records(raw_records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    # Validate all raw records and separate them into valid flights and errors.
    valid_flights: List[Dict[str, Any]] = []
    error_records: List[Dict[str, Any]] = []

    for record in raw_records:
        raw_line = record["raw"].strip()

        # Ignore completely empty lines.
        if not raw_line:
            continue

        # Comment lines are reported as errors with a clear explanation.
        if raw_line.startswith("#"):
            error_records.append(
                {
                    "file": record["file"],
                    "line_number": record["line_number"],
                    "raw": record["raw"],
                    "messages": ["comment line, ignored for data parsing"],
                }
            )
            continue

        # Header line is simply skipped without error.
        if is_header_line(raw_line):
            continue

        parts = [part.strip() for part in raw_line.split(",")]

        # There must be exactly six fields.
        if len(parts) != 6:
            error_records.append(
                {
                    "file": record["file"],
                    "line_number": record["line_number"],
                    "raw": record["raw"],
                    "messages": ["missing required fields"],
                }
            )
            continue

        flight_id, origin, destination, dep_text, arr_text, price_text = parts
        messages: List[str] = []

        validate_flight_id(flight_id, messages)
        validate_airport_code(origin, "origin", messages)
        validate_airport_code(destination, "destination", messages)

        dep_dt = parse_datetime(dep_text, "departure", messages)
        arr_dt = parse_datetime(arr_text, "arrival", messages)

        # Check ordering only if both datetimes are valid.
        if dep_dt is not None and arr_dt is not None:
            if arr_dt <= dep_dt:
                messages.append("arrival before departure")

        price_value = validate_price(price_text, messages)

        if messages:
            # At least one validation rule failed, keep as error.
            error_records.append(
                {
                    "file": record["file"],
                    "line_number": record["line_number"],
                    "raw": record["raw"],
                    "messages": messages,
                }
            )
            continue

        # If we reach this point the record is considered valid.
        valid_flights.append(
            {
                "flight_id": flight_id,
                "origin": origin,
                "destination": destination,
                "departure_datetime": dep_text,
                "arrival_datetime": arr_text,
                "price": price_value,
            }
        )

    return valid_flights, error_records
