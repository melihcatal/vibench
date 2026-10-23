import json

def validate_document_fields(document_data):
    required_fields = ["vendor", "date", "total"]
    for field in required_fields:
        if field not in document_data:
            return False, f"Missing required field: {field}"
    if "total" in document_data and not document_data["total"]:
        return False, "Total amount is missing"
    return True, "Validation passed"