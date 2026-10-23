import json

def normalize_expense(expense):
    normalized = {
        'vendor': expense.get('vendor', ''),
        'date': expense.get('date', ''),
        'total': expense.get('total', ''),
        'items': expense.get('items', [])
    }
    return json.dumps(normalized)