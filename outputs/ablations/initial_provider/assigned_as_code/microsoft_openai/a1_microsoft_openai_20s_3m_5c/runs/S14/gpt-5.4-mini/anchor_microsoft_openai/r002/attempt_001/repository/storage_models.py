def normalize_listing(items):
    normalized = []
    for item in items:
        normalized.append({
            'name': getattr(item, 'name', None),
            'size': getattr(item, 'size', None),
            'last_modified': getattr(item, 'last_modified', None),
            'etag': getattr(item, 'etag', None),
        })
    return normalized


def extract_text_payload(payload):
    if isinstance(payload, dict):
        return payload.get('text') or payload.get('content') or ''
    return str(payload) if payload is not None else ''


def build_metadata_document(blob_name, metadata=None, text=None):
    return {
        'object_name': blob_name,
        'metadata': metadata or {},
        'text': extract_text_payload(text),
    }
