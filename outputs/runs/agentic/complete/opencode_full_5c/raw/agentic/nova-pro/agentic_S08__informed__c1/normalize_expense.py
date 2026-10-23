def normalize_expense(expense):
    return {
        "vendor": expense.get("vendor", ""),
        "date": expense.get("date", ""),
        "total": expense.get("total", ""),
        "line_items": expense.get("line_items", []),
    }
