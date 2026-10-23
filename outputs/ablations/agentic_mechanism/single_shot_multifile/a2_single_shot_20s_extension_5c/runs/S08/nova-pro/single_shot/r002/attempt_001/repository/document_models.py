def normalize_expense_record(expense):
    return {
        'vendor': expense.get('vendor'),
        'date': expense.get('date'),
        'total': expense.get('total'),
        'items': [{'description': item.get('description'), 'amount': item.get('amount')} for item in expense.get('line_items', [])]
    }