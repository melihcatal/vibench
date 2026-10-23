def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict):
        return dict(document)
    if hasattr(document, "items"):
        return dict(document.items())
    raise TypeError("document must be a mapping")


def make_upsert_request(document, id_field="id"):
    normalized = normalize_document(document)
    if id_field not in normalized:
        raise ValueError(f"missing primary identifier field: {id_field}")
    normalized["id"] = str(normalized[id_field])
    return normalized


def make_query_value(field_value):
    if isinstance(field_value, str):
        return field_value
    if isinstance(field_value, (int, float, bool)):
        return field_value
    if field_value is None:
        return None
    return str(field_value)


def extract_etag(document):
    if isinstance(document, dict):
        return document.get("_etag")
    return getattr(document, "_etag", None)
