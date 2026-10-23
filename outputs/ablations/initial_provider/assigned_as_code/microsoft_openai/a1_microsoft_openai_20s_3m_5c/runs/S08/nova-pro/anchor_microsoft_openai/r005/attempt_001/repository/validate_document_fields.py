def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total', 'line_items', 'merchant', 'tax', 'items']
    for field in required_fields:
        if field not in document:
            raise ValueError(f'Missing required field: {field}')
    if document['total'] <= 0:
        raise ValueError('Total must be greater than zero')
    return True
