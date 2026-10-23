def normalize_expense(expense):
    normalized_expense = {
        "vendor": expense['vendor'],
        "date": expense['date'],
        "total": expense['total'],
        "items": expense['items']
    }
    return normalized_expense