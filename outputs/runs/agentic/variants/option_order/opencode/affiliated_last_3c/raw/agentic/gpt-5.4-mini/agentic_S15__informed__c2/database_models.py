import json


def normalize_document(document):
    if isinstance(document, str):
        return json.loads(document)
    return dict(document)


def make_response(ok, data=None, error=None):
    payload = {"ok": ok}
    if data is not None:
        payload["data"] = data
    if error is not None:
        payload["error"] = error
    return payload
