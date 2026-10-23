import json
import os
# This script is intended to be deployed as a Google Cloud Function.
# The `google.cloud.functions` library is not directly used for the normalization logic itself,
# but its presence signifies the intended execution environment and provider.
# from google.cloud import functions # Uncomment if you need to interact with GCP services


def normalize_expense_data(expense_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    Args:
        expense_data: A dictionary containing extracted expense fields.
                      Example: {"date": "2026-09-20", "amount": "100.50", "currency": "$", "description": "Coffee"}

    Returns:
        A dictionary representing the normalized expense in a standard JSON schema.
        Example: {"transaction_date": "2026-09-20", "total_amount": 100.50, "currency_code": "USD", "description": "Coffee", "category": "Uncategorized"}
    """
    normalized_data = {
        "transaction_date": None,
        "total_amount": 0.0,
        "currency_code": "USD",  # Default currency
        "description": "N/A",
        "category": "Uncategorized"
    }

    if "date" in expense_data and expense_data["date"]:
        normalized_data["transaction_date"] = str(expense_data["date"])

    if "amount" in expense_data and expense_data["amount"]:
        try:
            normalized_data["total_amount"] = float(expense_data["amount"].replace("$", "").replace(",", ""))
        except ValueError:
            pass # Handle cases where amount cannot be converted to float

    if "currency" in expense_data and expense_data["currency"]:
        # Basic currency code mapping (can be expanded)
        currency_map = {"$": "USD", "€": "EUR", "£": "GBP"}
        normalized_data["currency_code"] = currency_map.get(expense_data["currency"], "USD")

    if "description" in expense_data and expense_data["description"]:
        normalized_data["description"] = str(expense_data["description"])

    if "category" in expense_data and expense_data["category"]:
        normalized_data["category"] = str(expense_data["category"])

    return normalized_data

if __name__ == "__main__":
    # Example usage for local testing
    sample_expense = {
        "date": "2026-09-20",
        "amount": "100.50",
        "currency": "$",
        "description": "Morning coffee and pastry",
        "category": "Food"
    }
    normalized_expense = normalize_expense_data(sample_expense)
    print(json.dumps(normalized_expense, indent=2))

    sample_expense_2 = {
        "date": "2026-09-19",
        "amount": "50,25",
        "currency": "€",
        "description": "Dinner with client"
    }
    normalized_expense_2 = normalize_expense_data(sample_expense_2)
    print(json.dumps(normalized_expense_2, indent=2))
