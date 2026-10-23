from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
import copy


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_identifier(value: Any) -> str:
    if value is None:
        raise ValueError("identifier is required")
    text = str(value).strip()
    if not text:
        raise ValueError("identifier is required")
    return text


def normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("document must be a dict")
    return copy.deepcopy(document)


@dataclass
class DocumentUpsertRequest:
    document_id: str
    document: dict[str, Any]
    partition_key: str | None = None

    def to_storage_item(self) -> dict[str, Any]:
        item = normalize_document(self.document)
        item["id"] = normalize_identifier(self.document_id)
        if self.partition_key is not None:
            item["pk"] = str(self.partition_key)
        item.setdefault("version", 1)
        item["updated_at"] = utc_now_iso()
        item.setdefault("created_at", item["updated_at"])
        return item


@dataclass
class DocumentFetchRequest:
    document_id: str
    partition_key: str


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: str | None = None
    limit: int = 25


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    partition_key: str
    patch: dict[str, Any]
    expected_version: int | None = None
    condition_expression: str | None = None


@dataclass
class DocumentRecord:
    document_id: str
    partition_key: str | None
    version: int | None
    content: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_item(cls, item: dict[str, Any]) -> "DocumentRecord":
        return cls(
            document_id=str(item.get("id", "")),
            partition_key=item.get("pk"),
            version=item.get("version"),
            content=normalize_document(item),
        )


def filter_user_text_fields(document: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in document.items():
        if isinstance(value, str):
            result[key] = value
    return result
