from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Mapping, MutableMapping, Optional, Sequence
import json
import uuid


def _iso_utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _stable_uuid(value: Any) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))))


def normalize_document(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Decimal):
        if value == value.to_integral_value():
            return int(value)
        return float(value)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, Mapping):
        return {str(k): normalize_document(v) for k, v in value.items() if v is not None}
    if isinstance(value, (list, tuple, set, frozenset)):
        return [normalize_document(v) for v in value]
    return str(value)


def ensure_primary_id(document: Mapping[str, Any], primary_key: str = "id") -> dict[str, Any]:
    normalized = normalize_document(document)
    if not isinstance(normalized, dict):
        raise TypeError("document must normalize to a mapping")
    if primary_key not in normalized or normalized[primary_key] in (None, ""):
        normalized[primary_key] = _stable_uuid(normalized)
    return normalized


@dataclass(slots=True)
class DocumentRequest:
    collection: str
    document: Mapping[str, Any]
    primary_key: str = "id"
    idempotency_key: Optional[str] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> dict[str, Any]:
        payload = ensure_primary_id(self.document, self.primary_key)
        return payload


@dataclass(slots=True)
class DocumentQueryRequest:
    collection: str
    field: str
    value: Any
    limit: int = 100
    partition_key: Optional[str] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    def normalized_value(self) -> Any:
        return normalize_document(self.value)


@dataclass(slots=True)
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    patch: Mapping[str, Any]
    expected_version: Optional[int] = None
    condition_field: Optional[str] = None
    condition_value: Any = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    def normalized_patch(self) -> dict[str, Any]:
        return normalize_document(self.patch)


@dataclass(slots=True)
class DocumentResponse:
    ok: bool
    collection: str
    document: Optional[dict[str, Any]] = None
    documents: Sequence[dict[str, Any]] = field(default_factory=tuple)
    created_at: str = field(default_factory=_iso_utc_now)
    updated_at: str = field(default_factory=_iso_utc_now)
    version: Optional[int] = None
    request_id: Optional[str] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_document(cls, collection: str, document: Mapping[str, Any], *, version: Optional[int] = None, request_id: Optional[str] = None, ok: bool = True) -> "DocumentResponse":
        normalized = normalize_document(document)
        if not isinstance(normalized, dict):
            raise TypeError("document must normalize to a mapping")
        now = _iso_utc_now()
        return cls(ok=ok, collection=collection, document=normalized, created_at=now, updated_at=now, version=version, request_id=request_id)


@dataclass(slots=True)
class QueryResponse:
    ok: bool
    collection: str
    documents: Sequence[dict[str, Any]] = field(default_factory=tuple)
    count: int = 0
    request_id: Optional[str] = None
    metadata: MutableMapping[str, Any] = field(default_factory=dict)

    @classmethod
    def from_documents(cls, collection: str, documents: Sequence[Mapping[str, Any]], *, request_id: Optional[str] = None, ok: bool = True) -> "QueryResponse":
        normalized_docs = []
        for doc in documents:
            normalized = normalize_document(doc)
            if not isinstance(normalized, dict):
                raise TypeError("each document must normalize to a mapping")
            normalized_docs.append(normalized)
        return cls(ok=ok, collection=collection, documents=tuple(normalized_docs), count=len(normalized_docs), request_id=request_id)


@dataclass(slots=True)
class ErrorResponse:
    ok: bool
    error: str
    code: Optional[str] = None
    details: MutableMapping[str, Any] = field(default_factory=dict)
    request_id: Optional[str] = None


def build_document_payload(collection: str, document: Mapping[str, Any], primary_key: str = "id", idempotency_key: Optional[str] = None) -> DocumentRequest:
    return DocumentRequest(collection=collection, document=document, primary_key=primary_key, idempotency_key=idempotency_key)
