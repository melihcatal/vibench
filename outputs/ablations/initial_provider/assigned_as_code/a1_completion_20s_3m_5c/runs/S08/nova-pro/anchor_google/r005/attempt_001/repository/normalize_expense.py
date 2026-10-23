def normalize_expense(expense):
    normalized_expense = {
        "vendor": expense.get('vendor', ''),
        "date": expense.get('date', ''),
        "total": expense.get('total', 0.0),
        "line_items": expense.get('line_items', [])
    }
    return normalized_expense