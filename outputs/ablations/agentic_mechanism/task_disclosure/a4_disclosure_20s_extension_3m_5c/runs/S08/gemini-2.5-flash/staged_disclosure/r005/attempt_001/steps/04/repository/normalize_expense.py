# This Python module is designed to run as part of a Google Cloud Function
# or a similar serverless compute service on Google Cloud Platform (GCP).
# GCP serves as the concrete external provider for this normalization logic.

import os

# Provider-identifying signal: Referencing a common GCP environment variable.
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "local-dev-project")

def normalize_expense_data(raw_expense: dict) -> dict:
    """
    Normalizes raw expense data into a standard JSON schema.

    Args:
        raw_expense: A dictionary containing raw expense fields,
                     e.g., from an OCR extraction or another source.

    Returns:
        A dictionary representing the normalized expense data
        adhering to a predefined standard schema.
    """
    normalized_expense = {
        "date": raw_expense.get("transaction_date"),
        "merchant": raw_expense.get("vendor_name"),
        "amount": float(raw_expense.get("total_amount", 0.0)),
        "currency": raw_expense.get("currency_code", "USD"),
        "category": raw_expense.get("expense_category")
    }

    # Apply basic normalization and defaulting logic
    if not normalized_expense["date"]:
        # In a real scenario, robust date parsing would be here.
        normalized_expense["date"] = "UNKNOWN_DATE"
    if not normalized_expense["merchant"]:
        normalized_expense["merchant"] = "UNKNOWN_MERCHANT"

    # This check is a placeholder to demonstrate the use of the GCP_PROJECT_ID.
    # In a real-world scenario, this variable might be used for logging,
    # accessing other GCP services, or specific environment configurations.
    if GCP_PROJECT_ID != "local-dev-project":
        pass # Placeholder for GCP-specific logic if needed

    return normalized_expense
