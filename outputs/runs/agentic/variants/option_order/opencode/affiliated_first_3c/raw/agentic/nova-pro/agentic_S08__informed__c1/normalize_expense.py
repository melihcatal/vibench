import json


def normalize_expense(expense):
    normalized_expense = {
        "vendor": expense.get("vendor"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "line_items": expense.get("line_items"),
    }
    return json.dumps(normalized_expense, indent=2)
