import json


def normalize_expense(expense_data):
    normalized_data = {
        "vendor": expense_data["vendor"],
        "date": expense_data["date"],
        "total": expense_data["total"],
        "line_items": expense_data["line_items"],
    }
    return json.dumps(normalized_data)
