import json

def normalize_expense(data: dict) -> dict:
    normalized = {
        "vendor": data.get('vendor') or data.get('merchant'),
        "date": data.get('date'),
        "total": data.get('total'),
        "line_items": []
    }
    if 'line_items' in data:
        for item in data['line_items']:
            normalized['line_items'].append({
                "description": item.get('description') or item.get('name'),
                "quantity": item.get('quantity') or 1,
                "amount": item.get('amount') or item.get('price')
            })
    elif 'items' in data:
        for item in data['items']:
            normalized['line_items'].append({
                "description": item.get('name'),
                "quantity": item.get('quantity') or 1,
                "amount": item.get('price')
            })
    normalized['confidence'] = data.get('confidence')
    return normalized
