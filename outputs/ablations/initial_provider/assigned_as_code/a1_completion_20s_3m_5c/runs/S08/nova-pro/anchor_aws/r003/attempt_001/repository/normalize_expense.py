import json


def normalize_expense(expense):
    normalized_expense = {
        "vendor": expense.get("vendor"),
        "date": expense.get("date"),
        "total": expense.get("total"),
        "items": [
            {
                "description": item.get("description"),
                "quantity": item.get("quantity"),
                "amount": item.get("amount")
            }
            for item in expense.get("items", [])
        ]
    }
    return json.dumps(normalized_expense, default=str)