def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total', 'items']
    for field in required_fields:
        if field not in document or not document[field]:
            return False
    return True