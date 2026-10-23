def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total', 'line_items']
    for field in required_fields:
        if field not in document:
            return False
    return True
