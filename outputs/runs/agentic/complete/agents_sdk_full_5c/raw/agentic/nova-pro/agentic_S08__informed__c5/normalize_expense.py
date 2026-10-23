def normalize_expense(expense_data):
    normalized_expense = {
        'vendor': expense_data['vendor'],
        'date': expense_data['date'],
        'total': expense_data['total'],
        'items': expense_data['items']
    }
    return normalized_expense