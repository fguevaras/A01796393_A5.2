# Programming Assignment 5.2

## Overview
This program is a Python script that calculates the total cost of sales from a sales record file, based on prices from a product catalogue file. The program handles potential errors gracefully, such as missing files, malformed JSON, and invalid sales records (e.g., products not in the catalogue), by skipping them and logging a warning to the console.

## Project Structure
- **Source Code:** `source/compute_sales.py` - The main script for computing sales.
- **Unit Tests:** `tests/test_compute_sales.py` - Contains unit tests for the main script.
- **Product Catalogue:** `source/ProductList.json` - An example product catalogue file.
- **Results:** The program generates a `SalesResults.txt` file inside a `results/` directory.

## Requirements
- Python 3.x
- `pytest` (for running unit tests)
- `pylint` (for static code analysis)
- `flake8` (for style checking)

## Execution

### Running the Program
Run the program from the command line, providing the paths to the price catalogue and the sales record JSON files as command-line arguments.

```bash
python source/compute_sales.py <price_catalogue.json> <sales_record.json>
```

**Example:**
An example product catalogue is provided at `source/ProductList.json`. Assuming you have a sales record file named `sales.json`, you would run:
```bash
python source/compute_sales.py source/ProductList.json sales.json
```
The program will print the total cost to the console and save the output to `results/SalesResults.txt`.

### Running Tests
Unit tests are provided to verify the file loading, data processing, and calculation logic. To run the tests, ensure `pytest` is installed (`pip install pytest`) and run the following command from the project's root directory:
```bash
pytest -v
```

### Running Linters and Style Checks 
To ensure code quality and adherence to style guidelines, you can run pylint and flake8. 

Pylint 
```bash
pylint source/compute_sales.py
pylint tests/test_compute_sales.py
```

Flake8 
```bash
flake8 source/compute_sales.py
flake8 tests/test_compute_sales.py
```

## Author
- **Name:** Fabiola Guevara Soriano
- **ID:** A01796393
