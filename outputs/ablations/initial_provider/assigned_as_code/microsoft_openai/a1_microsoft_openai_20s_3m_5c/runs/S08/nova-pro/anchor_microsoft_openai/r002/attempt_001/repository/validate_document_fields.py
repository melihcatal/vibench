def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in document:
            raise ValueError(f'Missing required field: {field}')
    if 'line_items' not in document or not document['line_items']:
        raise ValueError('Missing line items')
    for item in document['line_items']:
        if 'description' not in item or 'quantity' not in item or 'amount' not in item:
            raise ValueError('Missing required fields in line item')