from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class DocumentRequest:
    document_id: str
    payload: Dict[str, Any] = field(default_factory=dict)
    partition_key: Optional[str] = None
    etag: Optional[str] = None


@dataclass
class DocumentResponse:
    document: Dict[str, Any]
    etag: Optional[str] = None
    status_code: Optional[int] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 25


@dataclass
class UpdateRequest:
    document_id: str
    updates: Dict[str, Any] = field(default_factory=dict)
    etag: Optional[str] = None
    partition_key: Optional[str] = None


@dataclass
class NormalizedRecord:
    document_id: str
    body: Dict[str, Any]
    partition_key: Optional[str] = None


def normalize_document(document: Mapping[str, Any], document_id_field: str = "id") -> NormalizedRecord:
    body = dict(document)
    document_id = str(body.get(document_id_field) or body.get("_id") or body.get("document_id") or "")
    if not document_id:
        raise ValueError("document_id is required")
    partition_key = body.get("partition_key") or body.get("pk")
    body[document_id_field] = document_id
    return NormalizedRecord(document_id=document_id, body=body, partition_key=partition_key)


def ensure_field(value: Mapping[str, Any], field_name: str) -> Any:
    if field_name not in value:
        raise KeyError(field_name)
    return value[field_name]


def merge_updates(original: Mapping[str, Any], updates: Mapping[str, Any]) -> Dict[str, Any]:
    merged = dict(original)
    for key, value in updates.items():
        merged[key] = value
    return merged


def sanitize_for_export(document: Mapping[str, Any], fields: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    if not fields:
        return dict(document)
    return {field: document.get(field) for field in fields}
