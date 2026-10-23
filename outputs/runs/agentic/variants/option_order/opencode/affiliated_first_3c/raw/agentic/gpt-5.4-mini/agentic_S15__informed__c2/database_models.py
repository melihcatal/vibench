from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_document_id(value: Any) -> str:
    if value is None:
        raise ValueError("document id is required")
    text = str(value).strip()
    if not text:
        raise ValueError("document id is required")
    return text


def normalize_document(data: Any) -> Dict[str, Any]:
    if data is None:
        return {}
    if isinstance(data, dict):
        return dict(data)
    raise TypeError("document must be a mapping")


@dataclass
class DocumentRequest:
    collection: str
    document_id: str
    document: Dict[str, Any]


@dataclass
class DocumentResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    items: Optional[List[Dict[str, Any]]] = None
    etag: Optional[str] = None
