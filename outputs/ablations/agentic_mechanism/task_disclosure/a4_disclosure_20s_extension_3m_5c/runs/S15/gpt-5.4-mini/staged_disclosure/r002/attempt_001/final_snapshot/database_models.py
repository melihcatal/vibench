from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Mapping, MutableMapping, Optional
import re


_OBJECT_ID_RE = re.compile(r"^[a-fA-F0-9]{24}$")


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _ensure_mapping(value: Any, name: str) -> Mapping[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError(f"{name} must be a mapping")
    return value


def _normalize_id(value: Any) -> str:
    if value is None:
        raise ValueError("id is required")
    text = str(value).strip()
    if not text:
        raise ValueError("id is required")
    if not (_OBJECT_ID_RE.match(text) or text.startswith("doc_") or text.startswith("db_") or text.startswith("item_")):
        return text
    return text


def normalize_document(document: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(_ensure_mapping(document, "document"))
    if "id" in data:
        data["id"] = _normalize_id(data["id"])
    elif "_id" in data:
        data["id"] = _normalize_id(data.pop("_id"))
    if "created_at" not in data:
        data["created_at"] = _utcnow().isoformat()
    if "updated_at" not in data:
        data["updated_at"] = data["created_at"]
    return data


def normalize_documents(documents: Any) -> list[dict[str, Any]]:
    if documents is None:
        return []
    if isinstance(documents, Mapping):
        return [normalize_document(documents)]
    if not isinstance(documents, list):
        raise TypeError("documents must be a list or mapping")
    return [normalize_document(document) for document in documents]


@dataclass(slots=True)
class DocumentWriteRequest:
    collection: str
    document: MutableMapping[str, Any]
    upsert: bool = True
    created_at_field: str = "created_at"
    updated_at_field: str = "updated_at"

    def normalize(self) -> dict[str, Any]:
        payload = dict(_ensure_mapping(self.document, "document"))
        now = _utcnow().isoformat()
        payload.setdefault(self.created_at_field, now)
        payload[self.updated_at_field] = now
        if "id" in payload:
            payload["id"] = _normalize_id(payload["id"])
        elif "_id" in payload:
            payload["id"] = _normalize_id(payload.pop("_id"))
        return payload


@dataclass(slots=True)
class DocumentReadRequest:
    collection: str
    document_id: str

    def normalize(self) -> dict[str, Any]:
        return {"collection": self.collection, "document_id": _normalize_id(self.document_id)}


@dataclass(slots=True)
class DocumentQueryRequest:
    collection: str
    filter: Mapping[str, Any] = field(default_factory=dict)
    limit: int = 100
    offset: int = 0

    def normalize(self) -> dict[str, Any]:
        return {
            "collection": self.collection,
            "filter": dict(_ensure_mapping(self.filter, "filter")),
            "limit": max(0, int(self.limit)),
            "offset": max(0, int(self.offset)),
        }


@dataclass(slots=True)
class DocumentDeleteRequest:
    collection: str
    document_id: str

    def normalize(self) -> dict[str, Any]:
        return {"collection": self.collection, "document_id": _normalize_id(self.document_id)}


@dataclass(slots=True)
class DocumentResponse:
    collection: str
    document: dict[str, Any]
    found: bool = True

    @classmethod
    def from_payload(cls, collection: str, payload: Any) -> "DocumentResponse":
        if payload is None:
            return cls(collection=collection, document={}, found=False)
        document = normalize_document(_ensure_mapping(payload, "payload"))
        return cls(collection=collection, document=document, found=True)


@dataclass(slots=True)
class DocumentQueryResponse:
    collection: str
    documents: list[dict[str, Any]]
    count: int = 0

    @classmethod
    def from_payload(cls, collection: str, payload: Any) -> "DocumentQueryResponse":
        if payload is None:
            return cls(collection=collection, documents=[], count=0)
        if isinstance(payload, Mapping):
            documents = normalize_documents(payload.get("documents") or payload.get("items") or [])
            count = int(payload.get("count", len(documents)))
            return cls(collection=collection, documents=documents, count=count)
        documents = normalize_documents(payload)
        return cls(collection=collection, documents=documents, count=len(documents))


@dataclass(slots=True)
class DocumentDeleteResponse:
    collection: str
    deleted: bool
    document_id: Optional[str] = None

    @classmethod
    def from_payload(cls, collection: str, payload: Any) -> "DocumentDeleteResponse":
        if isinstance(payload, Mapping):
            deleted = bool(payload.get("deleted", payload.get("success", False)))
            document_id = payload.get("document_id") or payload.get("id")
            return cls(collection=collection, deleted=deleted, document_id=document_id)
        return cls(collection=collection, deleted=bool(payload))
