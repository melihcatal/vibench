from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from database_client import document_id_field


@dataclass
class UpsertRequest:
    document: Dict[str, Any]


@dataclass
class FetchRequest:
    identifier: Any


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    identifier: Any
    expected_version: Optional[int]
    update_fields: Dict[str, Any]


@dataclass
class OperationResponse:
    ok: bool
    matched_count: int = 0
    modified_count: int = 0
    upserted_id: Any = None
    document: Optional[Dict[str, Any]] = None
    items: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""


def ensure_primary_identifier(document: Dict[str, Any]) -> Dict[str, Any]:
    if document_id_field() not in document:
        raise ValueError(f"Missing primary identifier field '{document_id_field()}'")
    return document


def normalize_record(record: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(record)
    if "_id" in normalized and "id" not in normalized:
        normalized["id"] = normalized["_id"]
    return normalized
