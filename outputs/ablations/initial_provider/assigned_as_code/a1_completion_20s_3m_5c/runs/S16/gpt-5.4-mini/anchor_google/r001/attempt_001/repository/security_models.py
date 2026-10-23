import json


def normalize_secret_value(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def parse_json_payload(value):
    value = normalize_secret_value(value)
    return json.loads(value)


def build_secret_response(field, value):
    return {field: value}
