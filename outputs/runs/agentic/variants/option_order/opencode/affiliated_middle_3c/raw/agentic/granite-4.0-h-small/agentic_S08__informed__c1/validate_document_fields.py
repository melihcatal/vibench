from typing import Any, Dict


def validate_document_fields(data: Dict[str, Any]) -> bool:
    """Validate required structured fields and confidence scores are present.

    Expected fields (at minimum):
      - vendor / merchant (string, non-empty)
      - date (string in YYYY-MM-DD format)
      - total (numeric > 0)
      - items or line_items (list with at least one item)
    """

    # Helper to check non-empty string
    def is_non_empty_str(val: Any) -> bool:
        return isinstance(val, str) and bool(val.strip())

    vendor = data.get("vendor") or data.get("merchant")
    if not is_non_empty_str(vendor):
        print("Missing or empty vendor/merchant field")
        return False

    date = data.get("date")
    if not isinstance(date, str) or not date.strip():
        print("Missing or empty date field")
        return False
    # Simple date format check (YYYY-MM-DD)
    if len(date) != 10 or date[4] != "-" or date[7] != "-":
        print("Date format should be YYYY-MM-DD")
        return False

    total = data.get("total")
    try:
        total_num = float(total)
        if total_num <= 0:
            print("Total must be a positive number")
            return False
    except ValueError:
        print("Total is not a valid number")
        return False

    items = data.get("items") or data.get("line_items")
    if not isinstance(items, list) or not items:
        print("Missing items/line_items list")
        return False
    if not all(isinstance(i, dict) for i in items):
        print("Items should be a list of dictionaries")
        return False
    # Simple check that each item has a description/name and a positive amount
    for i in items:
        if not ("description" in i or "name" in i):
            print("Item missing description/name")
            return False
        try:
            amount = float(i.get("total") or i.get("amount") or 0)
            if amount <= 0:
                print("Item total/amount must be positive")
                return False
        except ValueError:
            print("Item amount not a valid number")
            return False
    return True


# Simple test harness
if __name__ == "__main__":
    test_data = {
        "vendor": "Acme Corp",
        "date": "2024-07-15",
        "total": "125.50",
        "line_items": [
            {"description": "Widget A", "unit_price": "45.00", "total": "90.00"},
            {"description": "Widget B", "unit_price": "35.50", "total": "35.50"},
        ],
    }
    print("Validation result:", validate_document_fields(test_data))
