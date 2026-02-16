
# A01796393

"""
compute_sales.py

This script calculates the total cost of sales from a sales record file,
based on prices from a product catalogue file.

Usage:
    python compute_sales.py <path_to_price_catalogue> <path_to_sales_record>

Example:
    python compute_sales.py ProductList.json TC1/TC1.sales.json
"""

import json
import os
import sys
import time


def load_json_file(filepath):
    """
    Load and parse a JSON file.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        (list | dict | None): The parsed JSON data, or None if an error
                               occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found at '{filepath}'.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{filepath}'.")
    except OSError as e:
        print(f"An unexpected error occurred while reading '{filepath}': {e}")
    return None


def create_price_lookup(price_catalogue):
    """
    Create a dictionary for quick price lookups from the catalogue data.

    Args:
        price_catalogue (list): A list of product dictionaries.

    Returns:
        dict: A dictionary mapping product titles to their prices.
    """
    price_lookup = {}
    for item in price_catalogue:
        if isinstance(item, dict) and 'title' in item and 'price' in item:
            price_lookup[item['title']] = item['price']
        else:
            print(f"Warning: Skipping invalid item in price catalogue: {item}")
    return price_lookup


def compute_total_cost(price_lookup, sales_record):
    """
    Compute the total cost of all sales, handling errors in sales data.

    Args:
        price_lookup (dict): A dictionary of product prices.
        sales_record (list): A list of sale records.

    Returns:
        float: The total cost of all valid sales.
    """
    total_cost = 0.0
    for i, sale in enumerate(sales_record, 1):
        try:
            product_name = sale['Product']
            quantity = sale['Quantity']
            if product_name not in price_lookup:
                print(f"Warning: Product '{product_name}' from sale #{i} "
                      f"not in price catalogue. Skipping.")
                continue
            price = price_lookup[product_name]
            total_cost += price * quantity
        except (KeyError, TypeError) as e:
            print(f"Warning: Malformed sale record #{i}. Skipping. "
                  f"Error: {e}. Record: {sale}")
    return total_cost


def main():
    """Main function to run the sales computation program."""
    start_time = time.time()

    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <price_catalogue.json> "
              f"<sales_record.json>")
        sys.exit(1)

    price_catalogue_path = sys.argv[1]
    sales_record_path = sys.argv[2]

    price_catalogue_data = load_json_file(price_catalogue_path)
    sales_record_data = load_json_file(sales_record_path)

    if price_catalogue_data is None or sales_record_data is None:
        sys.exit(1)

    price_lookup = create_price_lookup(price_catalogue_data)
    total_cost = compute_total_cost(price_lookup, sales_record_data)
    elapsed_time = time.time() - start_time

    output_content = f"Total Cost: ${total_cost:,.2f}\n\n" \
        f"Execution Time: {elapsed_time:.4f} seconds\n"

    print(output_content)

    # Ensure the results directory exists and write the output file
    results_dir = "results"
    os.makedirs(results_dir, exist_ok=True)
    output_filepath = os.path.join(results_dir, "SalesResults.txt")

    with open(output_filepath, 'w', encoding='utf-8') as file:
        file.write(output_content)


if __name__ == "__main__":
    main()
