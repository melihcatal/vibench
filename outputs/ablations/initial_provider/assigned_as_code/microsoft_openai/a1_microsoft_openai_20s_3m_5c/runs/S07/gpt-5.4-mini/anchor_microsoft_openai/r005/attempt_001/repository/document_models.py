def normalize_text(text):
    return '\n'.join(line.rstrip() for line in (text or '').splitlines()).strip()


def normalize_payload(payload):
    payload = payload or {}
    return {
        'document_bytes': payload['document_bytes'],
        'mime_type': payload['mime_type'],
        'language': payload.get('language'),
        'formality': payload.get('formality'),
        'fields': payload.get('fields'),
    }


def normalize_result(result):
    return result
