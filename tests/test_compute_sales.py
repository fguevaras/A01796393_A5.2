# A01796393
# pylint: disable=redefined-outer-name

"""
Unit tests for the compute_sales script.
"""

import json
import pytest
from source import compute_sales


@pytest.fixture
def price_catalogue_data():
    """Fixture for sample price catalogue data."""
    return [
        {"title": "Product A", "price": 10.0},
        {"title": "Product B", "price": 25.5},
        {"title": "Product C", "price": 5.75},
    ]


def test_load_json_file_success(tmp_path):
    """Test loading a valid JSON file."""
    data = {"key": "value"}
    file_path = tmp_path / "test.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    loaded_data = compute_sales.load_json_file(str(file_path))
    assert loaded_data == data


def test_load_json_file_not_found(capsys):
    """Test loading a non-existent file."""
    result = compute_sales.load_json_file("non_existent_file.json")
    assert result is None
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out


def test_load_json_file_decode_error(tmp_path, capsys):
    """Test loading a malformed JSON file."""
    file_path = tmp_path / "malformed.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        # Use single quotes to create invalid JSON for the test
        f.write("{'key': 'value'}")

    result = compute_sales.load_json_file(str(file_path))
    assert result is None
    captured = capsys.readouterr()
    assert "Error: Could not decode JSON" in captured.out


def test_create_price_lookup(price_catalogue_data):
    """Test creating a price lookup dictionary from catalogue data."""
    expected_lookup = {
        "Product A": 10.0,
        "Product B": 25.5,
        "Product C": 5.75,
    }
    price_lookup = compute_sales.create_price_lookup(price_catalogue_data)
    assert price_lookup == expected_lookup


def test_create_price_lookup_with_invalid_item(capsys):
    """Test that invalid items in the catalogue are skipped."""
    invalid_catalogue = [
        {"title": "Valid Product", "price": 1.0},
        {"name": "Invalid Product", "cost": 2.0}  # Missing 'title'/'price'
    ]
    price_lookup = compute_sales.create_price_lookup(invalid_catalogue)
    assert "Valid Product" in price_lookup
    assert "Invalid Product" not in price_lookup
    captured = capsys.readouterr()
    assert "Warning: Skipping invalid item" in captured.out


def test_compute_total_cost(price_catalogue_data):
    """Test computing total cost with valid sales data."""
    price_lookup = compute_sales.create_price_lookup(price_catalogue_data)
    sales_record = [
        {"Product": "Product A", "Quantity": 2},  # 2 * 10.0 = 20.0
        {"Product": "Product C", "Quantity": 4},  # 4 * 5.75 = 23.0
    ]
    total_cost = compute_sales.compute_total_cost(price_lookup, sales_record)
    assert total_cost == pytest.approx(43.0)


def test_compute_total_cost_product_not_found(price_catalogue_data, capsys):
    """Test that sales for unknown products are skipped."""
    price_lookup = compute_sales.create_price_lookup(price_catalogue_data)
    sales_record = [
        {"Product": "Product A", "Quantity": 1},          # 10.0
        {"Product": "Unknown Product", "Quantity": 5},    # Skipped
    ]
    total_cost = compute_sales.compute_total_cost(price_lookup, sales_record)
    assert total_cost == pytest.approx(10.0)
    captured = capsys.readouterr()
    assert "not in price catalogue. Skipping" in captured.out


def test_compute_total_cost_malformed_sale(price_catalogue_data, capsys):
    """Test that malformed sale records are skipped."""
    price_lookup = compute_sales.create_price_lookup(price_catalogue_data)
    sales_record = [
        {"Product": "Product B", "Quantity": 1},  # 25.5
        {"Item": "Product C", "Count": 3},        # Malformed, skipped
    ]
    total_cost = compute_sales.compute_total_cost(price_lookup, sales_record)
    assert total_cost == pytest.approx(25.5)
    captured = capsys.readouterr()
    assert "Warning: Malformed sale record" in captured.out
