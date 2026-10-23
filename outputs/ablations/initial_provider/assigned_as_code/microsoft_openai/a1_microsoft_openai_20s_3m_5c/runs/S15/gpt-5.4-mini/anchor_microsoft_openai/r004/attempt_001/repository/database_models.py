def normalize_id(payload):
    if isinstance(payload, dict):
        return payload.get('id') or payload.get('document_id') or payload.get('pk')
    return payload


def normalize_document(payload):
    if isinstance(payload, dict):
        document = dict(payload.get('document') or payload)
        identifier = normalize_id(payload)
        if identifier is not None:
            document['id'] = identifier
        return document
    return {'id': payload}


def build_query(field, value):
    return {
        'query': 'SELECT * FROM c WHERE c["%s"] = @value' % field,
        'parameters': [{"name": "@value", "value": value}],
    }
