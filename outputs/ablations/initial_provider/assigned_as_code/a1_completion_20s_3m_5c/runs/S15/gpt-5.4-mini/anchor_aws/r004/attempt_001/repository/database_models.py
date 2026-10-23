import json
from decimal import Decimal


def to_json_safe(value):
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, dict):
        return {k: to_json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_json_safe(v) for v in value]
    return value


def normalize_document(document):
    return json.loads(json.dumps(document, default=str), parse_float=Decimal)


def build_response(item=None, **extra):
    response = {"document": to_json_safe(item) if item is not None else None}
    response.update(extra)
    return response
