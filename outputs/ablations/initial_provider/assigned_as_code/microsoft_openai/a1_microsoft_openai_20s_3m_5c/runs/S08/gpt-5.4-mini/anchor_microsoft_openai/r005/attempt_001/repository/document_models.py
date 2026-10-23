def _field_content(field):
    if field is None:
        return None
    if hasattr(field, 'content'):
        return field.content
    if isinstance(field, dict):
        return field.get('content') or field.get('value')
    return field


def _field_confidence(field):
    if field is None:
        return None
    if hasattr(field, 'confidence'):
        return field.confidence
    if isinstance(field, dict):
        return field.get('confidence')
    return None


def extract_fields_map(fields, keys):
    return {key: _field_content(fields.get(key)) for key in keys}


def confidence_map(fields, keys):
    return {key: _field_confidence(fields.get(key)) for key in keys}


def normalize_expense_record(record):
    return {
        'vendor': record.get('vendor'),
        'date': record.get('date'),
        'total': record.get('total'),
        'currency': record.get('currency') or 'USD',
        'line_items': record.get('line_items') or record.get('items') or [],
        'merchant': record.get('merchant'),
        'tax': record.get('tax'),
        'notes': record.get('notes') or record.get('memo'),
    }
