import json

def normalize_expense(expense_data):
    normalized_expense = {
        "vendor": expense_data.get("vendor"),
        "date": expense_data.get("date"),
        "total": expense_data.get("total"),
        "items": [
            {"description": item.get("description"), "quantity": item.get("quantity"), "amount": item.get("amount")}
            for item in expense_data.get("line_items", [])
        ]
    }
    return json.dumps(normalized_expense, indent=2)