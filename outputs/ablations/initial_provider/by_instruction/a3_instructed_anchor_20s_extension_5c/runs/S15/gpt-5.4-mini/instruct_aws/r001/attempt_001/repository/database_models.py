from dataclasses import dataclass


def normalize_item(item):
    if item is None:
        return None
    if isinstance(item, dict):
        return {k: normalize_item(v) for k, v in item.items()}
    if isinstance(item, list):
        return [normalize_item(v) for v in item]
    if isinstance(item, set):
        return [normalize_item(v) for v in sorted(item, key=lambda x: str(x))]
    return item


@dataclass
class DocumentRequest:
    document_id: str
    item: dict | None = None


@dataclass
class DocumentResponse:
    ok: bool
    data: dict | None = None
    error: str | None = None
