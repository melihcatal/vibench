import json


def maybe_json(value):
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        return json.loads(value)
    return value


def as_text(value):
    if value is None:
        return ''
    if isinstance(value, str):
        return value
    return json.dumps(value)


def pick_field(value, field=None):
    data = maybe_json(value)
    if field:
        return data[field]
    return data
