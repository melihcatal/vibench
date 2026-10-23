def normalize_expense(expense_fields):
    normalized_expense = {
        "vendor": expense_fields["vendor"],
        "date": expense_fields["date"].strftime("%Y-%m-%d"),
        "total": expense_fields["total"],
        "line_items": expense_fields["line_items"],
    }
    return normalized_expense
