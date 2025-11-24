# Flight Schedule Parser and Query Tool

Furkan Ciloglu  |  231ADB104

This is a small Python project for the Programming Languages course.  
The program can read flight schedule data from CSV files, validate each row, save valid flights to a JSON database and write invalid lines to a text file. It can also load an existing JSON database and run queries from a JSON file.

Everything is implemented with the Python standard library only.


## Features

- Parse a single CSV file with flight data
- Parse all `.csv` files from a directory
- Validate each record and separate valid and invalid rows
- Save valid flights to `db.json`
- Save invalid lines and comments to `errors.txt` with explanations
- Optionally load an existing JSON database file with `-j`
- Run queries from a JSON file with `-q`
- Save query results to a response JSON file with a timestamp in the file name


## Data format

### CSV input

Columns:

`flight_id,origin,destination,departure_datetime,arrival_datetime,price`

Example:

```text
BA2490,LHR,JFK,2025-11-14 10:30,2025-11-14 13:05,489.99
LH172,FRA,RIX,2025-11-12 07:15,2025-11-12 10:30,159.50
```


## Example Commands 

### Parse CSV and export

```python flight_parser.py -i data/db.csv```

### Parse multiple CSVs in folder

```python flight_parser.py -d data/flights/```

### Use existing JSON database

```python flight_parser.py -j db.json```

### Run queries from file

```python flight_parser.py -j db.json -q query.json```