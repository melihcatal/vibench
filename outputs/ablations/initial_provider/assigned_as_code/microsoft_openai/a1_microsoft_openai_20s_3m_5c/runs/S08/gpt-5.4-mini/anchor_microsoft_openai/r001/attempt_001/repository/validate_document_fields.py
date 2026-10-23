from document_models import field_content, field_confidence


def validate_document_fields(payload, config=None):
    config = config or {}
    fields = payload.get('fields') or {}
    required = config.get('required_fields') or ['merchant', 'vendor', 'date', 'total']
    minimum_confidence = config.get('minimum_confidence', 0.5)
    missing = [name for name in required if not field_content(fields, name)]
    low_confidence = [name for name in required if (field_confidence(fields, name) or 0) < minimum_confidence]
    return {'valid': not missing and not low_confidence, 'missing_fields': missing, 'low_confidence_fields': low_confidence}
