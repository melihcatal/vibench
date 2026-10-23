def normalize_expense(expense_fields):
    normalized_expense = {
        'vendor': expense_fields.get('Vendor', ''),
        'date': expense_fields.get('Date', ''),
        'total': expense_fields.get('Total', ''),
        'items': expense_fields.get('Items', [])
    }
    return normalized_expense