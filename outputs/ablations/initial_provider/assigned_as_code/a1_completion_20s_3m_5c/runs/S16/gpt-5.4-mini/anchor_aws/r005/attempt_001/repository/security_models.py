import json


def normalize_secret_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


def parse_json_secret(value):
    value = normalize_secret_text(value)
    return json.loads(value)


def select_field(data, field=None):
    if field:
        return data[field]
    return data
