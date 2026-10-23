from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Mapping, Optional, Union


JsonScalar = Union[str, int, float, bool, None]
JsonValue = Union[JsonScalar, Dict[str, Any], List[Any]]
Document = Dict[str, JsonValue]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _normalize_key(key: Any) -> str:
    if key is None:
        raise ValueError("Document keys must not be None")
    return str(key)


def _normalize_value(value: Any) -> JsonValue:
    if isinstance(value, dict):
        return normalize_document(value)
    if isinstance(value, list):
        return [
            _normalize_value(item)
            for item in value
        ]
    if isinstance(value, tuple):
        return [
            _normalize_value(item)
            for item in value
        ]
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def normalize_document(document: Mapping[Any, Any]) -> Document:
    return {
        _normalize_key(key): _normalize_value(value)
        for key, value in document.items()
    }


def normalize_documents(documents: Any) -> List[Document]:
    if documents is None:
        return []
    return [normalize_document(document) for document in documents]


@dataclass(frozen=True)
class ManagedNoSQLDocumentStoreRequest:
    collection: str
    document: Optional[Mapping[Any, Any]] = None
    document_id: Optional[str] = None
    query: Optional[Mapping[Any, Any]] = None
    limit: Optional[int] = None
    cursor: Optional[str] = None
    include_metadata: bool = False
    created_at: str = field(default_factory=_utc_now_iso)

    def normalized(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "collection": self.collection,
            "include_metadata": self.include_metadata,
            "created_at": self.created_at,
        }
        if self.document is not None:
            data["document"] = normalize_document(self.document)
        if self.document_id is not None:
            data["document_id"] = str(self.document_id)
        if self.query is not None:
            data["query"] = normalize_document(self.query)
        if self.limit is not None:
            data["limit"] = int(self.limit)
        if self.cursor is not None:
            data["cursor"] = str(self.cursor)
        return data


@dataclass(frozen=True)
class ManagedNoSQLDocumentStoreResponse:
    ok: bool
    collection: str
    document: Optional[Document] = None
    documents: List[Document] = field(default_factory=list)
    document_id: Optional[str] = None
    cursor: Optional[str] = None
    count: Optional[int] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_raw(cls, payload: Mapping[str, Any]) -> "ManagedNoSQLDocumentStoreResponse":
        document = payload.get("document")
        documents = payload.get("documents")
        metadata = payload.get("metadata") or {}
        return cls(
            ok=bool(payload.get("ok", True)),
            collection=str(payload.get("collection", "")),
            document=normalize_document(document) if isinstance(document, Mapping) else None,
            documents=normalize_documents(documents) if documents is not None else [],
            document_id=(str(payload["document_id"]) if payload.get("document_id") is not None else None),
            cursor=(str(payload["cursor"]) if payload.get("cursor") is not None else None),
            count=(int(payload["count"]) if payload.get("count") is not None else None),
            error=(str(payload["error"]) if payload.get("error") is not None else None),
            metadata=normalize_document(metadata) if isinstance(metadata, Mapping) else {},
        )

    def normalized(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {
            "ok": self.ok,
            "collection": self.collection,
            "documents": self.documents,
            "metadata": self.metadata,
        }
        if self.document is not None:
            data["document"] = self.document
        if self.document_id is not None:
            data["document_id"] = self.document_id
        if self.cursor is not None:
            data["cursor"] = self.cursor
        if self.count is not None:
            data["count"] = self.count
        if self.error is not None:
            data["error"] = self.error
        return data
