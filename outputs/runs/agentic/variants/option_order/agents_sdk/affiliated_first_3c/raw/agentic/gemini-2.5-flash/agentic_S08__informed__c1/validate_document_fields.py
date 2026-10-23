from typing import Dict, Any, List, Optional

def validate_document_fields(normalized_expense: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
    """
    Validates required structured fields and basic data quality for a normalized expense record.
    Returns a dictionary with validation status and any issues found.
    """
    validation_results = {
        "is_valid": True,
        "missing_fields": [],
        "invalid_data_types": [],
        "issues": []
    }

    # 1. Check for required fields
    for field in required_fields:
        if normalized_expense.get(field) is None or normalized_expense.get(field) == "":
            validation_results["is_valid"] = False
            validation_results["missing_fields"].append(field)
            validation_results["issues"].append(f"Missing required field: {field}")
    
    # 2. Basic data type and value validation for key fields
    # Validate total_amount
    total_amount = normalized_expense.get("total_amount")
    if total_amount is not None:
        if not isinstance(total_amount, (int, float)) or total_amount < 0:
            validation_results["is_valid"] = False
            validation_results["invalid_data_types"].append("total_amount")
            validation_results["issues"].append(f"Invalid total_amount: {total_amount}. Expected a positive number.")
    
    # Validate transaction_date (check if it's a string that could be a date, or an actual date object)
    transaction_date = normalized_expense.get("transaction_date")
    if transaction_date is not None and not isinstance(transaction_date, str):
        validation_results["is_valid"] = False
        validation_results["invalid_data_types"].append("transaction_date")
        validation_results["issues"].append(f"Invalid transaction_date: {transaction_date}. Expected a date string.")

    # Validate line_items structure (optional but good practice)
    line_items = normalized_expense.get("line_items")
    if line_items is not None and not isinstance(line_items, list):
        validation_results["is_valid"] = False
        validation_results["invalid_data_types"].append("line_items")
        validation_results["issues"].append(f"Invalid line_items: {line_items}. Expected a list.")
    elif isinstance(line_items, list):
        for i, item in enumerate(line_items):
            if not isinstance(item, dict):
                validation_results["is_valid"] = False
                validation_results["issues"].append(f"Line item at index {i} is not a dictionary.")
                continue
            # Validate item total if present
            item_total = item.get("total")
            if item_total is not None:
                if not isinstance(item_total, (int, float)) or item_total < 0:
                    validation_results["is_valid"] = False
                    validation_results["issues"].append(f"Invalid total for line item {i}: {item_total}. Expected a positive number.")

    return validation_results

if __name__ == "__main__":
    # Example usage
    valid_expense = {
        "document_type": "invoice",
        "vendor_name": "Tech Solutions Inc.",
        "transaction_date": "2023-10-26T00:00:00",
        "total_amount": 150.75,
        "currency": "USD",
        "tax_amount": 10.50,
        "line_items": [
            {"description": "Software License", "quantity": 1, "unit_price": 140.25, "total": 140.25},
            {"description": "Sales Tax", "quantity": 1, "unit_price": 10.50, "total": 10.50}
        ],
        "raw_extraction": {} # Omitted for brevity
    }

    invalid_expense = {
        "document_type": "receipt",
        "vendor_name": "", # Missing
        "transaction_date": "not-a-date", # Invalid format
        "total_amount": -10.00, # Invalid value
        "currency": "USD",
        "tax_amount": None,
        "line_items": ["bad_item"] # Invalid item type
    }

    required_fields_list = ["vendor_name", "transaction_date", "total_amount"]

    print("Valid expense validation:")
    results = validate_document_fields(valid_expense, required_fields_list)
    print(results)

    print("\nInvalid expense validation:")
    results = validate_document_fields(invalid_expense, required_fields_list)
    print(results)
