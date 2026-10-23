import json
from decimal import Decimal


def normalize_document(document):
    return json.loads(json.dumps(document), parse_float=Decimal)


def make_document_item(identifier, document, key_field="id"):
    item = normalize_document(document)
    item[key_field] = identifier
    return item


def response_from_item(item):
    return {"document": item, "found": item is not None}
