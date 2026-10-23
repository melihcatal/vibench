def normalize_document(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    return dict(payload)


def normalize_identifier(payload):
    if isinstance(payload, dict):
        return payload.get("id")
    return payload


def build_document_response(document_id, document):
    return {"id": document_id, "document": document}
