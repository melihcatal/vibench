def validate_document_fields(extracted, required_fields=None, min_confidence=0.5):
    required_fields = required_fields or ["vendor", "date", "total"]
    fields = getattr(extracted, "fields", {})
    errors = []
    for name in required_fields:
        field = fields.get(name)
        if field is None or getattr(field, "value", None) in (None, ""):
            errors.append(f"missing:{name}")
            continue
        if getattr(field, "confidence", 0.0) < min_confidence:
            errors.append(f"low_confidence:{name}")
    return {"valid": not errors, "errors": errors}
