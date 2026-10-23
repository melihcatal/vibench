def normalize_expense(expense_fields):
    return {
        "vendor": expense_fields["vendor"],
        "date": expense_fields["date"].isoformat(),
        "total": expense_fields["total"],
        "line_items": [
            {"description": item["description"], "amount": item["amount"]}
            for item in expense_fields["line_items"]
        ],
    }
