import json


def validate_document_fields(document):
    required_fields = ['vendor', 'date', 'total', 'items']
    errors = []
    for field in required_fields:
        if field not in document:
            errors.append(f'Missing required field: {field}')
        elif field == 'items' and not isinstance(document[field], list):
            errors.append(f'Invalid type for field: {field}')
    if errors:
        return json.dumps({'errors': errors}, indent=2)
    return json.dumps({'status': 'valid'}, indent=2)