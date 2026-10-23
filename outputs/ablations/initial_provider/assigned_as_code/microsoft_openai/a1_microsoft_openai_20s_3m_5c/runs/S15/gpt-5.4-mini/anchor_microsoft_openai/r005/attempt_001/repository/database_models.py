def normalize_document(document, document_id=None):
    normalized = dict(document or {})
    if document_id is not None:
        normalized['id'] = document_id
    return normalized


def build_query_parameters(field=None, value=None, key=None):
    if key is not None:
        return {'key': key}
    return {'field': field, 'value': value}


def extract_response_item(item):
    return dict(item) if item is not None else None


def build_versioned_update(document, updates, version_field='version'):
    merged = dict(document or {})
    merged.update(updates or {})
    if version_field in merged and isinstance(merged[version_field], int):
        merged[version_field] += 1
    return merged
