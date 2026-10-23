def normalize_expense(expense):
    normalized_expense = {
        'vendor': expense.get('vendor'),
        'date': expense.get('date'),
        'total': expense.get('total'),
        'items': [{'description': item['description'], 'amount': item['amount']} for item in expense.get('line_items', [])]
    }
    return normalized_expense