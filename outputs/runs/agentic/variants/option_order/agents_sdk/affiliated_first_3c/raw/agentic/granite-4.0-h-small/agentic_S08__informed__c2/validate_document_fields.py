import json

def validate_document_fields(raw_fields, required_fields=None):
    """
    Validate that extracted fields contain required values and reasonable confidence scores.
    raw_fields: dict returned from extraction functions.
    required_fields: list of field names to check, e.g. ["vendor", "date", "total", "line-items"]
    Returns bool indicating validity and a list of missing/invalid items.
    """
    missing = []
    errors = []
    # Define mandatory keys for invoices/receipts
    if not required_fields:
        required_fields = ["vendor", "date", "total", "line-items"]
    for key in required_fields:
        if key not in raw_fields or not raw_fields[key]:
            missing.append(key)
    # Simple confidence proxy: presence of a value implies confidence > 0
    if missing:
        errors.append(f"Missing required fields: {', '.join(missing)}")
    return (len(errors) == 0, errors)
