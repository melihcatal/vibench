def validate_document_fields(document_data):
    required_fields = ['vendor', 'date', 'total']
    for field in required_fields:
        if field not in document_data or not document_data[field]:
            return False
    return True