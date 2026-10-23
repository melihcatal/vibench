from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Any) -> Dict[str, Any]:
    if document is None:
        return {}
    if isinstance(document, dict):
        return document
    raise TypeError("document must be a mapping")


def document_key(document: Dict[str, Any], key_field: str = "id") -> str:
    value = document.get(key_field)
    if value is None:
        raise ValueError(f"missing key field: {key_field}")
    return str(value)


@dataclass
class DocumentUpsertRequest:
    collection: str
    document: Dict[str, Any]
    key_field: str = "id"


@dataclass
class DocumentFetchRequest:
    collection: str
    document_id: str


@dataclass
class DocumentQueryRequest:
    collection: str
    field_name: str
    field_value: Any


@dataclass
class DocumentConditionalUpdateRequest:
    collection: str
    document_id: str
    updates: Dict[str, Any]
    etag: Optional[str] = None
