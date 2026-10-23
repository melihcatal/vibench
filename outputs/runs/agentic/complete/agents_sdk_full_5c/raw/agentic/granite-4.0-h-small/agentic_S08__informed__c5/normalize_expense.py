def normalize_expense(expense_data):
    """Convert raw extraction results into a standard JSON schema."""
    return {
        "vendor": expense_data.get("vendor"),
        "date": expense_data.get("date"),
        "total": expense_data.get("total"),
        "items": expense_data.get("items", []),
        "confidence": {
            "vendor": expense_data.get("vendor_confidence", None),
            "date": expense_data.get("date_confidence", None),
            "total": expense_data.get("total_confidence", None),
            "items": expense_data.get("items_confidence", None)
        }
    }
