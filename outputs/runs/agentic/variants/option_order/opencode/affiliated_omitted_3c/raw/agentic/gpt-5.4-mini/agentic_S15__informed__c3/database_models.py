import json


def normalize_document(document):
    if document is None:
        return {}
    if isinstance(document, str):
        return json.loads(document)
    return dict(document)


def build_key(identifier, key_name="id"):
    return {key_name: identifier}


def response_payload(ok=True, **data):
    payload = {"ok": ok}
    payload.update(data)
    return payload
