from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


@dataclass
class DocumentKey:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class UpsertRequest:
    key: DocumentKey
    document: Dict[str, Any]
    table_name: Optional[str] = None


@dataclass
class FetchRequest:
    key: DocumentKey
    table_name: Optional[str] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    table_name: Optional[str] = None
    limit: int = 25


@dataclass
class ConditionalUpdateRequest:
    key: DocumentKey
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    table_name: Optional[str] = None


@dataclass
class OperationResponse:
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[Dict[str, Any]] = None



def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()



def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "updated_at" not in normalized:
        normalized["updated_at"] = utc_now_iso()
    if "created_at" not in normalized:
        normalized["created_at"] = normalized["updated_at"]
    if "version" not in normalized:
        normalized["version"] = 1
    return normalized



def merge_updates(original: Mapping[str, Any], updates: Mapping[str, Any]) -> Dict[str, Any]:
    merged = dict(original)
    merged.update(updates)
    merged["updated_at"] = utc_now_iso()
    merged["version"] = int(merged.get("version", 0)) + 1
    return merged
