import io


def normalize_payload(payload):
    if payload is None:
        payload = {}
    if isinstance(payload, dict):
        data = dict(payload)
    else:
        data = {'document_bytes': payload}
    document_bytes = data.get('document_bytes')
    if isinstance(document_bytes, io.BytesIO):
        document_bytes = document_bytes.getvalue()
    data['document_bytes'] = document_bytes
    data.setdefault('mime_type', 'application/octet-stream')
    return data


def normalize_text(text):
    if text is None:
        return ''
    if isinstance(text, str):
        return text.strip()
    return str(text).strip()
