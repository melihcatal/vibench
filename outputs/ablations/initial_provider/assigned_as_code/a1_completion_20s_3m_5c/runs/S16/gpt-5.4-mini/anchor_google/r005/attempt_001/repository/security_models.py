import json


def normalize_secret_payload(payload):
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except json.JSONDecodeError:
            return {"value": payload}
    return {"value": str(payload)}


def pick_field(payload, field):
    data = normalize_secret_payload(payload)
    return data[field] if field else data
