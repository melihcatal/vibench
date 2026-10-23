import json


def normalize_expense(expense):
    normalized_expense = {
        'vendor': expense.get('vendor', ''),
        'date': expense.get('date', ''),
        'total': expense.get('total', ''),
        'line_items': []
    }
    for item in expense.get('line_items', []):
        normalized_item = {
            'description': item.get('description', ''),
            'quantity': item.get('quantity', ''),
            'amount': item.get('amount', '')
        }
        normalized_expense['line_items'].append(normalized_item)
    return json.dumps(normalized_expense, indent=2)