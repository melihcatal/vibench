import json


def parse_json_payload(value):
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    if isinstance(value, str):
        return json.loads(value)
    return value


def extract_field(value, field=None):
    data = parse_json_payload(value)
    if field:
        return data[field]
    return data


def build_secret_result(name, value, metadata=None):
    result = {name: value}
    if metadata:
        result.update(metadata)
    return result
