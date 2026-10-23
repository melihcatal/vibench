import json


def normalize_secret_value(value):
    if isinstance(value, bytes):
        value = value.decode('utf-8')
    return value


def parse_json_secret_value(value):
    value = normalize_secret_value(value)
    return json.loads(value)


def extract_field(value, key_field=None):
    if key_field:
        return parse_json_secret_value(value)[key_field]
    return normalize_secret_value(value)


def secret_payload(secret_id, key_field=None, version=None, stage=None):
    return {'secret_id': secret_id, 'key_field': key_field, 'version': version, 'stage': stage}
