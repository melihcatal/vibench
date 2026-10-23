from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, Mapping, MutableMapping, Optional, Sequence


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _normalize_scalar(value: Any) -> Any:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, dict):
        return {str(k): _normalize_scalar(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [_normalize_scalar(v) for v in value]
    return value


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k): _normalize_scalar(v) for k, v in document.items()}


@dataclass(slots=True)
class DocumentCreateRequest:
    collection: str
    document: Dict[str, Any]
    document_id: Optional[str] = None
    partition_key: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "collection": self.collection,
            "document": normalize_document(self.document),
            "document_id": self.document_id,
            "partition_key": self.partition_key,
            "metadata": normalize_document(self.metadata),
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class DocumentUpdateRequest:
    collection: str
    document_id: str
    patch: Dict[str, Any]
    partition_key: Optional[str] = None
    upsert: bool = False

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "collection": self.collection,
            "document_id": self.document_id,
            "patch": normalize_document(self.patch),
            "partition_key": self.partition_key,
            "upsert": self.upsert,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class DocumentDeleteRequest:
    collection: str
    document_id: str
    partition_key: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "collection": self.collection,
            "document_id": self.document_id,
            "partition_key": self.partition_key,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class DocumentReadRequest:
    collection: str
    document_id: str
    partition_key: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "collection": self.collection,
            "document_id": self.document_id,
            "partition_key": self.partition_key,
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class QueryRequest:
    collection: str
    filter: Dict[str, Any] = field(default_factory=dict)
    limit: Optional[int] = None
    sort: Sequence[str] = field(default_factory=tuple)
    partition_key: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "collection": self.collection,
            "filter": normalize_document(self.filter),
            "limit": self.limit,
            "sort": list(self.sort),
            "partition_key": self.partition_key,
        }
        return {k: v for k, v in payload.items() if v not in (None, [], {})}


@dataclass(slots=True)
class DocumentResponse:
    ok: bool
    collection: str
    document: Dict[str, Any] = field(default_factory=dict)
    document_id: Optional[str] = None
    etag: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "DocumentResponse":
        data = dict(payload)
        created_at = data.get("created_at")
        updated_at = data.get("updated_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
        return cls(
            ok=bool(data.get("ok", True)),
            collection=str(data.get("collection", "")),
            document=dict(data.get("document", {})),
            document_id=data.get("document_id"),
            etag=data.get("etag"),
            created_at=created_at,
            updated_at=updated_at,
            raw=data,
        )

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "ok": self.ok,
            "collection": self.collection,
            "document": normalize_document(self.document),
            "document_id": self.document_id,
            "etag": self.etag,
            "created_at": _normalize_scalar(self.created_at),
            "updated_at": _normalize_scalar(self.updated_at),
        }
        return {k: v for k, v in payload.items() if v is not None}


@dataclass(slots=True)
class QueryResponse:
    ok: bool
    collection: str
    documents: list[Dict[str, Any]] = field(default_factory=list)
    count: int = 0
    continuation_token: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "QueryResponse":
        data = dict(payload)
        return cls(
            ok=bool(data.get("ok", True)),
            collection=str(data.get("collection", "")),
            documents=[dict(item) for item in data.get("documents", [])],
            count=int(data.get("count", len(data.get("documents", [])))),
            continuation_token=data.get("continuation_token"),
            raw=data,
        )

    def normalized(self) -> Dict[str, Any]:
        payload = {
            "ok": self.ok,
            "collection": self.collection,
            "documents": [normalize_document(doc) for doc in self.documents],
            "count": self.count,
            "continuation_token": self.continuation_token,
        }
        return {k: v for k, v in payload.items() if v is not None}


def build_document_record(collection: str, document: Mapping[str, Any], document_id: Optional[str] = None) -> Dict[str, Any]:
    record = normalize_document(document)
    record.setdefault("collection", collection)
    record.setdefault("document_id", document_id or record.get("id") or record.get("_id"))
    record.setdefault("created_at", _utc_now().isoformat().replace("+00:00", "Z"))
    record.setdefault("updated_at", record["created_at"])
    return record
