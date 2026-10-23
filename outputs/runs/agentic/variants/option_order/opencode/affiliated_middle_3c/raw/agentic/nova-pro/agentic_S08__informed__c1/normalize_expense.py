def normalize_expense(expense_data):
    return {
        "vendor": expense_data["vendor"],
        "date": expense_data["date"],
        "total": expense_data["total"],
        "items": [
            {"description": item["description"], "amount": item["amount"]}
            for item in expense_data["line_items"]
        ],
    }
