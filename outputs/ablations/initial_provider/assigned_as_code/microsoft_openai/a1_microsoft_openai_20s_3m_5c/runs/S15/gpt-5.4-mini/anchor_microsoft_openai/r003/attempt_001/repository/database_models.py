def build_document_id(payload):
    return payload['id']


def build_document(payload):
    document = dict(payload.get('document', {}))
    document['id'] = payload['id']
    return document


def normalize_query_result(items):
    return [dict(item) for item in items]


def build_update_patch(payload):
    return payload.get('patch', {})
