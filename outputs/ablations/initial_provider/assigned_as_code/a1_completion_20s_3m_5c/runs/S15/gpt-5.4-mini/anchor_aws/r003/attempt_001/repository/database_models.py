import json
from dataclasses import dataclass
from decimal import Decimal


def _json_default(value):
    if isinstance(value, Decimal):
        return float(value)
    raise TypeError


def normalize_document(document):
    if document is None:
        return None
    return json.loads(json.dumps(document, default=_json_default), parse_float=Decimal)


@dataclass
class DocumentRef:
    id: str


@dataclass
class DocumentQuery:
    field: str
    value: object


@dataclass
class UpdateRequest:
    id: str
    document: dict
    expected_version: object = None
