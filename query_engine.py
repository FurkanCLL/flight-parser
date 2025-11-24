# Furkan Ciloglu  |  231ADB104
# Query processing functions for flight database.

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any


def load_queries(path: Path) -> List[Dict[str, Any]]:
    # Load query definitions from a JSON file.
    try:
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        raise SystemExit(f"Error: Invalid JSON format in query file {path}")

    # The query file can be a single object or a list of objects.
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data

    raise SystemExit("Error: Query file must contain an object or a list of objects")


def match_flight(flight: Dict[str, Any], query: Dict[str, Any]) -> bool:
    # Check if a single flight matches the given query rules.

    for key, value in query.items():

        if key in ["flight_id", "origin", "destination"]:
            if flight.get(key) != value:
                return False

        elif key == "price":
            if float(flight.get("price", 0)) > float(value):
                return False

        elif key == "departure_datetime":
            flight_dt = datetime.strptime(
                flight["departure_datetime"], "%Y-%m-%d %H:%M"
            )
            query_dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
            if flight_dt < query_dt:
                return False

        elif key == "arrival_datetime":
            flight_dt = datetime.strptime(
                flight["arrival_datetime"], "%Y-%m-%d %H:%M"
            )
            query_dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
            if flight_dt > query_dt:
                return False

    return True


def execute_queries(
    flights: List[Dict[str, Any]],
    queries: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    # Execute each query and collect matching flights.

    results = []

    for query in queries:
        matches = []

        for flight in flights:
            if match_flight(flight, query):
                matches.append(flight)

        results.append(
            {
                "query": query,
                "matches": matches,
            }
        )

    return results
