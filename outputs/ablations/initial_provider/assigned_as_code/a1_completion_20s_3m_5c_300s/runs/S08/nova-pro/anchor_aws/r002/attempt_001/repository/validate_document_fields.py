def validate_document_fields(document):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in document:
            return False
        if not document[field]:
            return False
    if "line_items" not in document or not document["line_items"]:
        return False
    for item in document["line_items"]:
        if "description" not in item or "quantity" not in item or "amount" not in item:
            return False
    return True