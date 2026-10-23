import json


def normalize_secret_value(value):
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def parse_json_payload(value):
    return json.loads(normalize_secret_value(value))
