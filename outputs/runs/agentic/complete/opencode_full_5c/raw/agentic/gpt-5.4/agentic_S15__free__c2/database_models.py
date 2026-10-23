from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Optional


@dataclass
class DocumentKey:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class DocumentWriteRequest:
    document_id: str
    body: Dict[str, Any]
    partition_key: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 100


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and not isinstance(normalized["id"], str):
        normalized["id"] = str(normalized["id"])
    return normalized


def ensure_document_identity(document_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
    normalized = normalize_document(body)
    normalized["id"] = str(document_id)
    return normalized


def summarize_documents(documents: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    items = [normalize_document(item) for item in documents]
    fields = sorted({key for item in items for key in item.keys()})
    return {"count": len(items), "fields": fields, "documents": items}
