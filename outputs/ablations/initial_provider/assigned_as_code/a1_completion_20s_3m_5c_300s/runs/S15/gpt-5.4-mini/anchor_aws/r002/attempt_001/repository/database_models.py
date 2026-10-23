import json
from decimal import Decimal


def normalize_document(document):
    return json.loads(json.dumps(document), parse_float=Decimal)


def build_key(payload, config):
    key_field = config.get("key_field", "id")
    key = {key_field: payload["id"]}
    sort_field = config.get("sort_field")
    if sort_field and sort_field in payload:
        key[sort_field] = payload[sort_field]
    return key


def to_response(item=None, **extra):
    response = dict(extra)
    if item is not None:
        response["document"] = item
    return response
