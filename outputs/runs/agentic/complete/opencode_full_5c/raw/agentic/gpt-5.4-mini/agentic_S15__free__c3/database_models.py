import base64
import json
from decimal import Decimal


def _normalize(value):
    if isinstance(value, Decimal):
        if value % 1 == 0:
            return int(value)
        return float(value)
    if isinstance(value, bytes):
        return base64.b64encode(value).decode("ascii")
    if isinstance(value, dict):
        return {k: _normalize(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize(v) for v in value]
    return value


def normalize_item(item):
    return _normalize(item or {})


def parse_json_document(document):
    if isinstance(document, str):
        return json.loads(document)
    return document


def build_success_response(item=None, consumed_capacity=None, message=None):
    payload = {"ok": True}
    if item is not None:
        payload["item"] = normalize_item(item)
    if consumed_capacity is not None:
        payload["consumed_capacity"] = normalize_item(consumed_capacity)
    if message is not None:
        payload["message"] = message
    return payload


def build_error_response(error):
    return {"ok": False, "error": str(error)}
