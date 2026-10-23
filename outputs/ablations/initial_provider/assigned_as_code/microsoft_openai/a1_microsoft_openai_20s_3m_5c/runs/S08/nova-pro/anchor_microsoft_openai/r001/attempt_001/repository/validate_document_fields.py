def validate_document_fields(document_fields):
    required_fields = ['vendor', 'date', 'total', 'line_items']
    missing_fields = [field for field in required_fields if field not in document_fields]
    if missing_fields:
        raise ValueError(f'Missing required fields: {missing_fields}')
    for item in document_fields.get('line_items', []):
        if not all(key in item for key in ['description', 'quantity', 'amount']):
            raise ValueError('Line items must contain description, quantity, and amount fields')
    return True