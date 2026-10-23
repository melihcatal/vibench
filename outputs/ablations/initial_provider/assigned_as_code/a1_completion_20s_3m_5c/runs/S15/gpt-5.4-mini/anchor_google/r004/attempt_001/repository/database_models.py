def normalize_document(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return dict(payload)


def build_document_response(document_id, document):
    return {"id": document_id, "document": normalize_document(document)}


def build_query_response(documents):
    return {"documents": [build_document_response(item["id"], item["document"]) for item in documents]}
