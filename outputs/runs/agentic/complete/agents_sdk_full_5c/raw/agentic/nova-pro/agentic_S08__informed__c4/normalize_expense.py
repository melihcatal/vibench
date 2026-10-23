def normalize_expense(expense):
    return {
        'vendor': expense['vendor'],
        'date': expense['date'].strftime('%Y-%m-%d'),
        'total': expense['total'].units,
        'currency': expense['total'].currency_code,
        'line_items': expense['line_items']
    }
