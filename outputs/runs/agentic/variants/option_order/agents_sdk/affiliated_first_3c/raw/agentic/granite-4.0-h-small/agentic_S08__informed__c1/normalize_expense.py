def normalize_expense(expense_data: dict) -> dict:
    """
    Normalizes extracted fields (invoice or receipt) into a common JSON schema:
    {
        'vendor': str,
        'date': str,
        'total': float,
        'line_items': [dict(description, amount, quantity, tax)]
    }
    """
    normalized = {
        'vendor': expense_data.get('vendor') or expense_data.get('merchant'),
        'date': expense_data.get('date'),
        'total': float(expense_data.get('total') or 0),
        'line_items': []
    }
    # Extract items - source may differ (line_items, items etc.)
    items = expense_data.get('line_items') or expense_data.get('items') or []
    for it in items:
        normalized['line_items'].append({
            'description': it.get('description') or it.get('name'),
            'amount': float(it.get('amount') or 0),
            'quantity': it.get('quantity') or 1,
            'tax': float(it.get('tax') or 0)
        })
    return normalized
