"""Request/response normalization helpers for Azure Cosmos DB documents."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document_payload(payload: Mapping[str, Any], id_field: str = "id") -> Dict[str, Any]:
    doc = dict(payload)
    if id_field not in doc or not doc[id_field]:
        raise ValueError(f"Missing required primary identifier field: {id_field}")
    doc["id"] = str(doc[id_field])
    doc.setdefault("created_at", utc_now_iso())
    doc["updated_at"] = utc_now_iso()
    return doc


def normalize_query_value(value: Any) -> Any:
    if isinstance(value, str):
        return value.strip()
    return value


@dataclass
class DocumentResponse:
    id: str
    document: Dict[str, Any]
    etag: Optional[str] = None
    status: str = "ok"

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueryResponse:
    documents: List[Dict[str, Any]] = field(default_factory=list)
    count: int = 0
    status: str = "ok"

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UpdateResult:
    id: str
    updated: bool
    document: Dict[str, Any]
    status: str = "ok"

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)
