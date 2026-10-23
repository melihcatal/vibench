def validate_document_fields(extracted_fields):
    required_fields = ['Vendor', 'Date', 'Total']
    for field in required_fields:
        if field not in extracted_fields:
            return False
    return True