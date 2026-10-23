from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class DocumentRecord:
    id: str
    partition_key: str
    data: Dict[str, Any] = field(default_factory=dict)
    etag: Optional[str] = None
    ts: Optional[int] = None

    def to_item(self) -> Dict[str, Any]:
        item = {"id": self.id, "partition_key": self.partition_key, **self.data}
        return item


@dataclass
class UpsertDocumentRequest:
    id: str
    partition_key: str
    document: Dict[str, Any]


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    id: str
    partition_key: str
    expected_etag: Optional[str]
    patch: Dict[str, Any]


@dataclass
class ServiceResponse:
    ok: bool
    payload: Dict[str, Any]
    error: Optional[str] = None


def normalize_document(item: Mapping[str, Any]) -> DocumentRecord:
    known = {k: v for k, v in item.items() if k not in {"id", "partition_key", "_etag", "_ts"}}
    return DocumentRecord(
        id=str(item.get("id", "")),
        partition_key=str(item.get("partition_key", "")),
        data=known,
        etag=item.get("_etag"),
        ts=item.get("_ts"),
    )


def as_iso_utc(ts: Optional[int] = None) -> str:
    dt = datetime.fromtimestamp(ts or datetime.now(tz=timezone.utc).timestamp(), tz=timezone.utc)
    return dt.isoformat()
