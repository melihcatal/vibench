def normalize_expense(expense):
    normalized_expense = {
        "vendor": expense.get("vendor"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "items": expense.get("items"),
    }
    return normalized_expense