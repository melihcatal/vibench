def validate_document_fields(document_fields):
    required_fields = ["vendor", "date", "total", "line_items"]
    for field in required_fields:
        if field not in document_fields:
            raise ValueError(f"Missing required field: {field}")
        if (
            "confidence" in document_fields[field]
            and document_fields[field]["confidence"] < 0.5
        ):
            raise ValueError(f"Low confidence for field: {field}")
    return True
