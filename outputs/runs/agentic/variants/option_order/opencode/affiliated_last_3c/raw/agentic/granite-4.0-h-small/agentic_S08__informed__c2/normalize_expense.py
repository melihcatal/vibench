import json


def normalize_expense(expense):
    # expense is dict from same-scenario extractors
    normalized = {
        "vendor_or_merchant": expense.get("vendor", expense.get("merchant", "")),
        "date": expense.get("date", ""),
        "total": expense.get("total", ""),
        "line_items": [],
        "tax": expense.get("tax", ""),
    }
    if "line_items" in expense:
        for item in expense["line_items"]:
            normalized["line_items"].append(
                {
                    "description": item.get("description", ""),
                    "quantity": 1,  # placeholder
                    "price": "",  # placeholder
                }
            )
    elif "items" in expense:
        for item in expense["items"]:
            normalized["line_items"].append(
                {"description": item.get("name", ""), "quantity": 1, "price": ""}
            )
    return normalized
