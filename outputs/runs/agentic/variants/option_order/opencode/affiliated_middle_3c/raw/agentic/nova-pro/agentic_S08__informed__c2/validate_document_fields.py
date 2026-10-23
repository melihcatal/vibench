def validate_document_fields(extracted_data):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in extracted_data or not extracted_data[field]:
            return False
    return True
