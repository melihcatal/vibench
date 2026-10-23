def normalize_expense(expense_fields):
    normalized_expense = {
        "vendor": expense_fields.get("vendor"),
        "date": expense_fields.get("date"),
        "total": expense_fields.get("total"),
        "line_items": expense_fields.get("line_items", []),
    }
    return normalized_expense
