def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict):
        return dict(document)
    return dict(document.__dict__)


def build_document_id(payload):
    return payload['id']


def build_query_filter(field, value):
    return {'field': field, 'value': value}


def build_condition(version=None, etag=None):
    condition = {}
    if version is not None:
        condition['version'] = version
    if etag is not None:
        condition['etag'] = etag
    return condition
