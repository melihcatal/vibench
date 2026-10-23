from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
import json


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document_id(value: Any) -> str:
    if value is None:
        raise ValueError("document id is required")
    text = str(value).strip()
    if not text:
        raise ValueError("document id is required")
    return text


def normalize_partition_key(value: Any) -> str:
    if value is None:
        raise ValueError("partition key is required")
    text = str(value).strip()
    if not text:
        raise ValueError("partition key is required")
    return text


def normalize_document(payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise TypeError("payload must be a dictionary")
    normalized = json.loads(json.dumps(payload, default=str))
    normalized["id"] = normalize_document_id(normalized.get("id"))
    partition_key = (
        normalized.get("partition_key")
        or normalized.get("tenant_id")
        or normalized.get("user_id")
    )
    normalized["partition_key"] = normalize_partition_key(partition_key)
    normalized.setdefault("updated_at", utc_now_iso())
    normalized.setdefault("created_at", normalized["updated_at"])
    return normalized


@dataclass(slots=True)
class DocumentLookup:
    document_id: str
    partition_key: str

    @classmethod
    def from_values(cls, document_id: Any, partition_key: Any) -> "DocumentLookup":
        return cls(
            document_id=normalize_document_id(document_id),
            partition_key=normalize_partition_key(partition_key),
        )


@dataclass(slots=True)
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: str | None = None
    limit: int = 50

    def normalized(self) -> "QueryRequest":
        field_name = self.field_name.strip()
        if not field_name:
            raise ValueError("field_name is required")
        if self.limit < 1:
            raise ValueError("limit must be positive")
        return QueryRequest(
            field_name=field_name,
            field_value=self.field_value,
            partition_key=normalize_partition_key(self.partition_key)
            if self.partition_key is not None
            else None,
            limit=self.limit,
        )


@dataclass(slots=True)
class ConditionalUpdateRequest:
    document_id: str
    partition_key: str
    updates: dict[str, Any]
    etag: str | None = None

    def normalized(self) -> "ConditionalUpdateRequest":
        if not isinstance(self.updates, dict) or not self.updates:
            raise ValueError("updates must be a non-empty dictionary")
        return ConditionalUpdateRequest(
            document_id=normalize_document_id(self.document_id),
            partition_key=normalize_partition_key(self.partition_key),
            updates=json.loads(json.dumps(self.updates, default=str)),
            etag=self.etag,
        )


@dataclass(slots=True)
class OperationResult:
    provider: str
    success: bool
    document: dict[str, Any] | None = None
    documents: list[dict[str, Any]] | None = None
    request_charge: float | None = None
    etag: str | None = None
