import json


def normalize_document(document):
    if isinstance(document, str):
        return json.loads(document)
    if isinstance(document, dict):
        return dict(document)
    raise TypeError("document must be a dict or JSON string")


def normalize_id(value):
    if value is None:
        raise ValueError("id is required")
    return str(value)


def upsert_result(item):
    return {"document": item}


def fetch_result(item):
    return {"document": item}


def query_result(items):
    return {"documents": items}


def update_result(item):
    return {"document": item}
