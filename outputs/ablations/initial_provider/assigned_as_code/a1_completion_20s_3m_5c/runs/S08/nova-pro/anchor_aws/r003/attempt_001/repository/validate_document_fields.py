import json


def validate_document_fields(document):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in document:
            return False
    if "items" not in document or not isinstance(document["items"], list):
        return False
    for item in document["items"]:
        if not all(key in item for key in ["description", "quantity", "amount"]):
            return False
    return True