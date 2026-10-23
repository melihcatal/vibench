# [SAME-SCENARIO] normalize_expense.py

# Local helper to map extracted fields to a standard JSON schema

from typing import Dict, Any, List

StandardExpense = Dict[str, Any]

STANDARD_SCHEMA = {
    "vendor_or_merchant": str,
    "date": str,
    "total": str,
    "line_items_or_items": List[Dict[str, Any]],
}


def normalize_expense(extracted: Dict[str, Any]) -> StandardExpense:
    """Normalize invoice or receipt dict to a common expense schema.

    Expected keys from SDK responses:
    - invoice: vendor, invoice_date, total_amount, line_items
    - receipt: merchant, tax_amount, total_amount, items
    """
    result: StandardExpense = {
        "vendor_or_merchant": extracted.get("vendor") or extracted.get("merchant"),
        "date": extracted.get("invoice_date") or extracted.get("date"),
        "total": extracted.get("total_amount") or extracted.get("total"),
        "line_items_or_items": extracted.get("line_items") or extracted.get("items"),
    }
    # Basic validation - ensure required fields exist
    required = ["vendor_or_merchant", "date", "total", "line_items_or_items"]
    missing = [r for r in required if not result.get(r)]
    if missing:
        raise ValueError(f"Missing required normalized fields: {missing}")
    return result
