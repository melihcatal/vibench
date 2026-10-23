import json


def normalize_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        try:
            return json.loads(payload)
        except Exception:
            return {'text': payload}
    return payload


def build_message_body(payload):
    return json.dumps(normalize_payload(payload))


def message_attributes(payload, defaults=None):
    data = normalize_payload(payload)
    attrs = dict(defaults or {})
    if isinstance(data, dict):
        for key in ('id', 'type', 'source', 'tenant'):
            if key in data and key not in attrs:
                attrs[key] = str(data[key])
    return attrs
