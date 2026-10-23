import json
from decimal import Decimal


def normalize_document(document):
    return json.loads(json.dumps(document), parse_float=Decimal)


def build_key(payload, config=None):
    config = config or {}
    key_field = config.get("key_field", "id")
    return {key_field: payload[key_field]}


def document_from_item(item):
    return json.loads(json.dumps(item, default=str))
