from decimal import Decimal


def normalize_value(value):
    if isinstance(value, float):
        return Decimal(str(value))
    if isinstance(value, dict):
        return {k: normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalize_value(v) for v in value]
    return value


def normalize_document(document):
    return normalize_value(document)


def build_document_response(
    item=None, consumed_capacity=None, count=None, next_token=None
):
    payload = {"item": item, "consumed_capacity": consumed_capacity}
    if count is not None:
        payload["count"] = count
    if next_token is not None:
        payload["next_token"] = next_token
    return payload


def build_status_response(ok, data=None, error=None):
    return {"ok": ok, "data": data, "error": error}
