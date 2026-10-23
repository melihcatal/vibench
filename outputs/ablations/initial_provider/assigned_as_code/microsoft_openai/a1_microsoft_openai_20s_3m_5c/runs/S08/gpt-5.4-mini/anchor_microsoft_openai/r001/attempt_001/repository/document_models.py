def field_content(fields, key):
    value = (fields or {}).get(key)
    return value.content if value else None


def field_confidence(fields, key):
    value = (fields or {}).get(key)
    return value.confidence if value else None


def normalize_documents(documents, field_names):
    normalized = []
    for document in documents or []:
        fields = document.fields or {}
        item = {name: field_content(fields, name) for name in field_names}
        item['confidences'] = {name: field_confidence(fields, name) for name in field_names}
        normalized.append(item)
    return normalized
