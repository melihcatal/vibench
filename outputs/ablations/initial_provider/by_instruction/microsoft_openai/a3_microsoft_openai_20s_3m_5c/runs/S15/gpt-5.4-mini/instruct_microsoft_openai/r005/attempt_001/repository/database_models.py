import os


def _normalize_value(value):
    if isinstance(value, dict):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    return value


def normalize_document(document):
    return _normalize_value(document)


def normalize_identifier(identifier):
    if isinstance(identifier, dict):
        return normalize_document(identifier)
    return {"id": identifier}


def build_response(ok, data=None, error=None):
    payload = {"ok": bool(ok)}
    if data is not None:
        payload["data"] = normalize_document(data)
    if error is not None:
        payload["error"] = str(error)
    return payload


def load_json_env(name, default=None):
    value = os.getenv(name)
    if not value:
        return default
    return value
