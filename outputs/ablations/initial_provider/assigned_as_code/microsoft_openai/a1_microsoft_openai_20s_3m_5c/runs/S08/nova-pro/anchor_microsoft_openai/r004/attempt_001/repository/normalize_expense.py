import json


def normalize_expense(expense):
    normalized_expense = {
        'vendor': expense.get('vendor'),
        'date': expense.get('date'),
        'total': expense.get('total'),
        'items': []
    }
    for item in expense.get('line_items', []) or expense.get('items', []):
        normalized_item = {
            'description': item.get('description'),
            'quantity': item.get('quantity'),
            'amount': item.get('amount')
        }
        normalized_expense['items'].append(normalized_item)
    return json.dumps(normalized_expense, indent=2)