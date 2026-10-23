import json


def document_key(document_id):
    return {"document_id": str(document_id)}


def normalize_item(item):
    if item is None:
        return None
    if isinstance(item, str):
        try:
            return json.loads(item)
        except Exception:
            return {"value": item}
    return dict(item)


def upsert_request(document_id, payload, version=None):
    data = normalize_item(payload)
    data["document_id"] = str(document_id)
    if version is not None:
        data["version"] = int(version)
    return data


def record_response(item):
    return {"record": normalize_item(item)}
