from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional


@dataclass(slots=True)
class DocumentRecord:
    id: str
    data: Dict[str, Any] = field(default_factory=dict)
    etag: Optional[str] = None
    version: Optional[int] = None


@dataclass(slots=True)
class UpsertRequest:
    collection: str
    document_id: str
    payload: Dict[str, Any]


@dataclass(slots=True)
class QueryRequest:
    collection: str
    field_name: str
    field_value: Any


@dataclass(slots=True)
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None


@dataclass(slots=True)
class ServiceResult:
    ok: bool
    document: Optional[DocumentRecord] = None
    documents: list[DocumentRecord] = field(default_factory=list)
    message: str = ""


def normalize_payload(payload: Mapping[str, Any] | MutableMapping[str, Any] | None) -> Dict[str, Any]:
    if not payload:
        return {}
    return {str(k): v for k, v in dict(payload).items() if v is not None}


def normalize_text_fields(payload: Mapping[str, Any], fields: Iterable[str]) -> Dict[str, Any]:
    normalized = dict(payload)
    for field_name in fields:
        value = normalized.get(field_name)
        if isinstance(value, str):
            normalized[field_name] = value.strip()
    return normalized
