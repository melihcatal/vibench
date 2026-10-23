def normalize_document(document):
    if document is None:
        return None
    if hasattr(document, "to_dict"):
        document = document.to_dict()
    if isinstance(document, dict):
        normalized = dict(document)
        normalized.setdefault("id", normalized.get("id"))
        return normalized
    return document


def build_query_filter(field, value):
    return {"field": field, "value": value}


def build_update_payload(document_id, updates, version=None):
    payload = {"id": document_id, "updates": dict(updates)}
    if version is not None:
        payload["version"] = version
    return payload
