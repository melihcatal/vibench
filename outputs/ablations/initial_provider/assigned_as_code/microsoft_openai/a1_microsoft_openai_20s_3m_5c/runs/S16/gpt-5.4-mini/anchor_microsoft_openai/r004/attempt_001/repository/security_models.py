import json


def load_payload(payload):
    if payload is None:
        return {}
    if isinstance(payload, str):
        return json.loads(payload)
    return dict(payload)


def normalize_secret_value(value):
    if value is None:
        return ''
    if isinstance(value, bytes):
        return value.decode('utf-8')
    return str(value)


def select_field(data, field):
    if not field:
        return data
    return data[field]
