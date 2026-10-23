import json

def normalize_expense(extracted):
    '''Convert vendor/receipt extraction result into a standard expense JSON schema.'''
    normalized = {
        'expense_id': None,               # to be set downstream
        'merchant': extracted.get('vendor') or extracted.get('merchant'),
        'date': extracted.get('date'),
        'amount': extracted.get('total', 0.0),
        'line_items': extracted.get('line_items') or extracted.get('items'),
        'category': None,                 # domain-specific categorization logic can be added
        'tax': extracted.get('tax', 0.0),
        'confidence': extracted.get('confidence', 1.0),  # placeholder
    }
    return json.loads(json.dumps(normalized))  # ensure clean dict (optional)
