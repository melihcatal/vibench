import os
import requests
import json

EXPENSE_NORMALIZATION_API_URL = os.getenv("EXPENSE_NORMALIZATION_API_URL", "https://api.expensenormalization.com/v1/normalize")
EXPENSE_NORMALIZATION_API_KEY = os.getenv("EXPENSE_NORMALIZATION_API_KEY")

def normalize_expense(raw_expense_data: dict) -> dict:
    """
    Normalizes extracted expense fields into a standard JSON schema.

    Args:
        raw_expense_data: A dictionary containing the raw extracted expense fields.

    Returns:
        A dictionary representing the normalized expense data conforming to a standard JSON schema.
    """
    if not EXPENSE_NORMALIZATION_API_KEY:
        print("Warning: EXPENSE_NORMALIZATION_API_KEY not set. Using local normalization only.")

    normalized_data = {
        "id": raw_expense_data.get("id"),
        "vendor": raw_expense_data.get("merchant_name"),
        "date": raw_expense_data.get("transaction_date"),
        "amount": {
            "value": float(raw_expense_data.get("total_amount", 0)),
            "currency": raw_expense_data.get("currency_code", "USD").upper()
        },
        "category": raw_expense_data.get("expense_category"),
        "description": raw_expense_data.get("item_description")
    }

    # Example of integrating with an external normalization API
    # In a real scenario, you would send the raw_expense_data to the API
    # and then process its response.
    try:
        headers = {"Authorization": f"Bearer {EXPENSE_NORMALIZATION_API_KEY}", "Content-Type": "application/json"}
        # For demonstration, we're sending the already locally normalized data.
        # In a real system, you might send raw_expense_data to the external API
        # and then further process the API's response.
        response = requests.post(EXPENSE_NORMALIZATION_API_URL, headers=headers, json=normalized_data, timeout=5)
        response.raise_for_status()
        external_api_result = response.json()

        # Merge or override with external API results if necessary
        # For this example, we'll assume the external API returns a more refined version
        # of the normalized data.
        normalized_data.update(external_api_result.get("normalized_fields", {}))

    except requests.exceptions.RequestException as e:
        print(f"Error calling external normalization API: {e}")
        # Continue with locally normalized data if API call fails

    return normalized_data

if __name__ == "__main__":
    # Example Usage
    sample_raw_expense = {
        "id": "exp_123",
        "merchant_name": "Starbucks",
        "transaction_date": "2026-09-20",
        "total_amount": "5.50",
        "currency_code": "usd",
        "expense_category": "Food & Beverage",
        "item_description": "Coffee and pastry"
    }

    print("Raw Expense Data:")
    print(json.dumps(sample_raw_expense, indent=2))

    normalized_expense = normalize_expense(sample_raw_expense)

    print("\nNormalized Expense Data:")
    print(json.dumps(normalized_expense, indent=2))
