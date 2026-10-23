REQUIRED_FIELDS = {
    'invoice': ['vendor', 'date', 'total', 'line_items'],
    'receipt': ['merchant', 'tax', 'total', 'items']
}

def validate_document_fields(extracted, doc_type):
    """
    Ensure required fields are present and confidence score meets threshold.
    Returns (valid: bool, missing: list, low_confidence: bool)
    """
    req = REQUIRED_FIELDS.get(doc_type)
    if not req:
        return False, [], False
    missing = [f for f in req if not extracted.get(f)]
    # Simple confidence check (e.g., 0.8 threshold)
    confidence_low = extracted.get('confidence') is not None and extracted['confidence'] < 0.8
    valid = not missing and not confidence_low
    return valid, missing, confidence_low