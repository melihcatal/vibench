REQUIRED_FIELDS = {"vendor", "date", "total", "items"}


def validate_document_fields(fields):
    """Check that required structured fields and confidence scores exist."""
    if not isinstance(fields, dict):
        raise ValueError("Fields must be a dict")
    missing = REQUIRED_FIELDS - fields.keys()
    if missing:
        raise ValueError(f"Missing required fields: {missing}")
    # Simple confidence check: each confidence value should be 0-1 or None
    for key, conf in fields.get("confidence", {}).items():
        if conf is not None and (conf < 0 or conf > 1):
            raise ValueError(f"Confidence for {key} out of range: {conf}")
    return True
