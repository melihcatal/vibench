# normalize_expense.py
# Helper to standardize extracted expense fields into a unified JSON schema
import json


def normalize_expense(expense_data):
    """Convert provider-specific expense response into a standard schema.

    Args:
        expense_data (dict): Raw response from any provider (invoice or receipt).
    Returns:
        dict: Normalized JSON with consistent keys.
    """
    normalized = {
        "vendor_or_merchant": expense_data.get("vendor")
        or expense_data.get("merchant"),
        "date": expense_data.get("date"),
        "total": expense_data.get("total"),
        "currency": expense_data.get("currency"),
        "line_items": [],
        "items": [],
        "tax": expense_data.get("tax"),
    }
    # Merge line-items from different structures
    if "line_items" in expense_data:
        normalized["line_items"] = expense_data["line_items"]
    if "items" in expense_data:
        normalized["items"] = expense_data["items"]
    return normalized
