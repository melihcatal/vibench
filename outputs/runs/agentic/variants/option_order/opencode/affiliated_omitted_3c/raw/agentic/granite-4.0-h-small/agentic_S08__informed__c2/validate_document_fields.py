import json

REQUIRED_FIELDS = [("vendor",), ("merchant",), ("date",), ("total",), ("line_items",)]


def validate_document_fields(doc: dict):
    """
    Validate that required structured fields and confidence scores are present.
    Returns True if valid, raises ValueError with details otherwise.
    """
    for fields in REQUIRED_FIELDS:
        if not any(field in doc for field in fields):
            raise ValueError(f"Missing required field(s): {', '.join(fields)}")
    # Simple confidence check; real scenario would inspect model confidence
    if doc.get("confidence", 0) < 0.8:
        raise ValueError(f"Low confidence score: {doc.get('confidence')} < 0.8")
    return True
