import json

def normalize_expense(expense):
    normalized_expense = {
        'vendor': expense['vendor'],
        'date': expense['date'],
        'total': expense['total'],
        'line_items': expense['line_items'],
        'merchant': expense['merchant'],
        'tax': expense['tax'],
        'items': expense['items']
    }
    return json.dumps(normalized_expense, indent=2)
