from document_models import field_content, field_confidence


def normalize_expense(payload, config=None):
    config = config or {}
    fields = payload.get('fields') or {}
    return {
        'source': config.get('source', 'azure-document-intelligence'),
        'merchant': field_content(fields, 'merchant'),
        'vendor': field_content(fields, 'vendor'),
        'date': field_content(fields, 'date'),
        'total': field_content(fields, 'total'),
        'tax': field_content(fields, 'tax'),
        'line_items': payload.get('line_items') or [],
        'confidence': {
            'merchant': field_confidence(fields, 'merchant'),
            'vendor': field_confidence(fields, 'vendor'),
            'date': field_confidence(fields, 'date'),
            'total': field_confidence(fields, 'total'),
            'tax': field_confidence(fields, 'tax')
        }
    }
