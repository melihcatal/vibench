def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict) and 'id' in document:
        return document
    return dict(document)


def build_document_payload(doc_id, document):
    payload = normalize_document(document) or {}
    payload['id'] = doc_id
    return payload


def build_query_params(field_name, field_value):
    return {'field_name': field_name, 'field_value': field_value}
