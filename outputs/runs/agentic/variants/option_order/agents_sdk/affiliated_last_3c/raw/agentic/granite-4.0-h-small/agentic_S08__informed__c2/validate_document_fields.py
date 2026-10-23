def validate_document_fields(extracted, required_fields):
    """Check that extracted dict contains all required fields with non‑empty values.
    Also optionally verify confidence scores if present (e.g., extracted[field]['confidence']).
    "+""
    missing = [f for f in required_fields if not extracted.get(f)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    # Example confidence check (optional)
    # for f, value in extracted.items():
    #     if isinstance(value, dict) and 'confidence' in value:
    #         if value['confidence'] < 0.7:
    #             raise ValueError(f"Low confidence for {f}: {value['confidence']}")
    return True
