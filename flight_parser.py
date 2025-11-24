# Furkan Ciloglu  |  231ADB104
# Flight Schedule Parser and Query Tool
# This module handles command line arguments and basic setup.

import argparse
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime

from csv_loader import read_csv_file, read_csv_from_directory
from validator import validate_records
from storage import save_valid_flights, save_error_records, save_query_response
from json_loader import load_flights_from_json
from query_engine import load_queries, execute_queries

def parse_arguments() -> argparse.Namespace:
    # Configure and parse command line arguments.
    parser = argparse.ArgumentParser(
        description="Flight schedule parser and query tool."
    )

    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Path to a single CSV file."
    )

    parser.add_argument(
        "-d",
        "--directory",
        type=str,
        help="Path to a directory that contains CSV files."
    )

    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Optional path for the valid flights JSON file. Default is db.json."
    )

    parser.add_argument(
        "-j",
        "--json",
        type=str,
        help="Path to an existing JSON database file. "
             "If this is provided, CSV parsing is skipped."
    )

    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Path to a JSON file that contains queries."
    )

    args = parser.parse_args()
    return args


def validate_arguments(args: argparse.Namespace) -> None:
    # Perform basic validation on the combination of arguments.
    has_json = args.json is not None
    has_input = args.input is not None
    has_dir = args.directory is not None

    if has_json and (has_input or has_dir):
        raise SystemExit(
            "Error: You cannot use -j/--json together with -i/--input or -d/--directory."
        )

    if not has_json and not (has_input or has_dir):
        raise SystemExit(
            "Error: You must provide either -j/--json or at least one of -i/--input or -d/--directory."
        )


def resolve_paths(args: argparse.Namespace) -> Dict[str, Optional[Path]]:
    # Convert string paths from arguments into Path objects.
    csv_file: Optional[Path] = Path(args.input) if args.input else None
    csv_dir: Optional[Path] = Path(args.directory) if args.directory else None
    json_db: Optional[Path] = Path(args.json) if args.json else None
    query_file: Optional[Path] = Path(args.query) if args.query else None

    if args.output:
        output_json = Path(args.output)
    else:
        output_json = Path("db.json")

    return {
        "csv_file": csv_file,
        "csv_dir": csv_dir,
        "json_db": json_db,
        "query_file": query_file,
        "output_json": output_json,
    }


def check_input_paths(paths: Dict[str, Optional[Path]]) -> None:
    # Check if the provided input paths exist on the file system.
    csv_file = paths["csv_file"]
    csv_dir = paths["csv_dir"]
    json_db = paths["json_db"]
    query_file = paths["query_file"]

    if csv_file is not None and not csv_file.is_file():
        raise SystemExit(f"Error: CSV file not found: {csv_file}")

    if csv_dir is not None and not csv_dir.is_dir():
        raise SystemExit(f"Error: Directory not found: {csv_dir}")

    if json_db is not None and not json_db.is_file():
        raise SystemExit(f"Error: JSON database file not found: {json_db}")

    if query_file is not None and not query_file.is_file():
        raise SystemExit(f"Error: Query file not found: {query_file}")


def load_raw_records(paths: Dict[str, Optional[Path]]) -> List[Dict[str, Any]]:
    # Decide how to load data based on the arguments.
    csv_file = paths["csv_file"]
    csv_dir = paths["csv_dir"]
    json_db = paths["json_db"]

    if json_db is not None:
        return load_flights_from_json(json_db)

    if csv_file is not None:
        return read_csv_file(csv_file)

    if csv_dir is not None:
        return read_csv_from_directory(csv_dir)

    return []


def main() -> None:
    # Main entry point of the program.
    args = parse_arguments()
    validate_arguments(args)
    paths = resolve_paths(args)
    check_input_paths(paths)

    if paths["json_db"] is not None:
        valid_flights = load_flights_from_json(paths["json_db"])
        error_records = []
        raw_records = valid_flights
    else:
        raw_records = load_raw_records(paths)
        valid_flights, error_records = validate_records(raw_records)

    # Save outputs.
    output_json_path = paths["output_json"]
    save_valid_flights(valid_flights, output_json_path)

    errors_path = Path("errors.txt")
    save_error_records(error_records, errors_path)

    print("Flight tool configuration:")
    print(f"  CSV file:       {paths['csv_file']}")
    print(f"  CSV directory:  {paths['csv_dir']}")
    print(f"  JSON database:  {paths['json_db']}")
    print(f"  Output JSON:    {paths['output_json']}")
    print(f"  Query file:     {paths['query_file']}")
    print()
    print(f"Total raw records:   {len(raw_records)}")
    print(f"Valid flight count:  {len(valid_flights)}")
    print(f"Error record count:  {len(error_records)}")
    print(f"Saved valid flights to: {output_json_path}")
    print(f"Saved errors to:        {errors_path}")

    # If a query file is provided, execute it on the loaded flights.
    if paths["query_file"] is not None:
        queries = load_queries(paths["query_file"])
        results = execute_queries(valid_flights, queries)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        response_name = f"response_Furkan_Ciloglu_{timestamp}.json"
        response_path = Path(response_name)

        save_query_response(results, response_path)

        print()
        print(f"Query results saved to: {response_path}")

if __name__ == "__main__":
    main()
