import json


def normalize_secret_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            parsed = json.loads(payload)
            return parsed if isinstance(parsed, dict) else {'value': parsed}
        except json.JSONDecodeError:
            return {'value': payload}
    return {'value': payload}


def extract_field(payload, key_field=None):
    data = normalize_secret_payload(payload)
    if key_field:
        return data[key_field]
    return data
