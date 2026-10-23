from document_models import confidence_map


def validate_document_fields(payload, config=None):
    document = payload.get('document') or {}
    fields = document.get('fields') or {}
    required = payload.get('required_fields') or ['vendor', 'date', 'total']
    confidences = confidence_map(fields, required)
    missing = [field for field in required if not fields.get(field)]
    low_confidence = [field for field, value in confidences.items() if value is not None and value < payload.get('min_confidence', 0.8)]
    return {'valid': not missing and not low_confidence, 'missing_fields': missing, 'low_confidence_fields': low_confidence, 'field_confidences': confidences}
