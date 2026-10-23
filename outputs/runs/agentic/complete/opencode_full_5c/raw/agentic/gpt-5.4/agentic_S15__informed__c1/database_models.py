from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(document)
    if "id" in normalized and normalized["id"] is not None:
        normalized["id"] = str(normalized["id"])
    return normalized


@dataclass(slots=True)
class DocumentUpsertRequest:
    document_id: str
    payload: dict[str, Any]

    def to_item(self) -> dict[str, Any]:
        item = normalize_document(self.payload)
        item["id"] = self.document_id
        if "version" not in item:
            item["version"] = 1
        if "updated_at" not in item:
            item["updated_at"] = utc_now_iso()
        return item


@dataclass(slots=True)
class DocumentFetchResponse:
    found: bool
    document: dict[str, Any] | None = None


@dataclass(slots=True)
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    limit: int = 25


@dataclass(slots=True)
class ConditionalUpdateRequest:
    document_id: str
    expected_version: int
    updates: dict[str, Any] = field(default_factory=dict)

    def build_updated_document(
        self, current_document: dict[str, Any]
    ) -> dict[str, Any]:
        merged = normalize_document(current_document)
        merged.update(normalize_document(self.updates))
        merged["id"] = self.document_id
        merged["version"] = int(current_document.get("version", 0)) + 1
        merged["updated_at"] = utc_now_iso()
        return merged
