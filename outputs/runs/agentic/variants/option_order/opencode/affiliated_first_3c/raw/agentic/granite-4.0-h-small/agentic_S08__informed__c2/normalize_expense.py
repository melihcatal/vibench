# normalize_expense.py
# [SAME-SCENARIO]
# Normalizes extracted expense fields into a standard JSON schema.

import json
from typing import Dict, List, Any


def normalize_expense(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize raw expense data to a standard format.

    The expected keys may vary based on provider (e.g., vendor vs merchant).
    This helper abstracts them into a unified schema.

    Args:
        raw_data: Raw output from invoice or receipt extraction.

    Returns:
        A normalized dict with keys: vendor_or_merchant, date, total, tax, items, line_items.
    """
    # Extract common fields with sensible defaults
    vendor_or_merchant = (
        raw_data.get("vendor") or raw_data.get("merchant") or "Unknown Merchant"
    )
    date = raw_data.get("date") or raw_data.get("date_est") or ""
    total = raw_data.get("total") or raw_data.get("amountTotal") or 0.0
    tax = raw_data.get("tax") or raw_data.get("taxAmount") or 0.0
    # Items may be in line_items or items list depending on provider
    items: List[str] = []
    if "line_items" in raw_data:
        for li in raw_data["line_items"]:
            # Assume each line_item has a description and amount
            desc = li.get("description", "").strip()
            amount = str(li.get("amount", 0))
            items.append(f"{desc} - ${amount}")
    elif "items" in raw_data:
        for it in raw_data["items"]:
            items.append(f"{it.get('item', '')} - ${it.get('price', 0)}")
    else:
        # Fallback - assume single raw text description
        items.append(f"{raw_data.get('description', 'No items')} - $0.0")
    return {
        "vendor_or_merchant": vendor_or_merchant,
        "date": date,
        "total": float(total),
        "tax": float(tax),
        "line_items": items,
        "items": items,  # include flat list view
    }


# Example usage
if __name__ == "__main__":
    sample = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": "150.00",
        "line_items": [
            {"description": "Office Supplies", "amount": 75.0},
            {"description": "Consulting", "amount": 75.0},
        ],
    }
    normalized = normalize_expense(sample)
    print(json.dumps(normalized, indent=2))
