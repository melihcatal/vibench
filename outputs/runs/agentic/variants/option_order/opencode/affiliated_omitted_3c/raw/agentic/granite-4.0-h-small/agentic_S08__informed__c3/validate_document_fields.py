import json
import re
from typing import Dict, Any


def validate_document_fields(expense_json: str) -> bool:
    # Load JSON payload
    try:
        expense = json.loads(expense_json)
    except json.JSONDecodeError:
        return False
    # Required top‑level fields
    required_fields = {"vendor", "date", "total", "line_items"}
    if not required_fields.issubset(expense):
        return False
    # Basic validation of each field
    if not isinstance(expense["vendor"], str) or not expense["vendor"].strip():
        return False
    if not re.match(r"\\d{4}[-/]?\\d{1,2}[-/]?\\d{1,2}", expense["date"]):
        return False
    if not re.match(r"[\\d.]+", expense["total"]):
        return False
    # Validate line_items list
    if not isinstance(expense["line_items"], list):
        return False
    for li in expense["line_items"]:
        if "amount" not in li or not re.match(r"[\\d.]+", li["amount"]):
            return False
        # Optional vendor/description checks
        if "vendor" in li and not isinstance(li["vendor"], str):
            return False
        if "description" in li and not isinstance(li["description"], str):
            return False
    # Optional but nice‑to‑have
    if "tax" in expense and not re.match(r"[\\d.]+", expense["tax"]):
        return False
    return True
