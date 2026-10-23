import json


def normalize_secret_text(value):
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return str(value)


def parse_json_secret(value):
    return json.loads(normalize_secret_text(value))


def build_secret_result(name, value, version=None):
    result = {name: value}
    if version is not None:
        result["version"] = version
    return result


def extract_key(data, key_field):
    return data[key_field] if key_field else data
