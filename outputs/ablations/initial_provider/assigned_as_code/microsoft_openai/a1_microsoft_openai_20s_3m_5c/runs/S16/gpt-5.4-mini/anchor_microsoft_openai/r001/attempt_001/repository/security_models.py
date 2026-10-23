import json


def normalize_secret_value(value):
    if isinstance(value, (dict, list)):
        return value
    try:
        return json.loads(value)
    except Exception:
        return value


def build_response(**kwargs):
    return dict(kwargs)
