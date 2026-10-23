def validate_document_fields(document_fields):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in document_fields:
            return False
    return True
