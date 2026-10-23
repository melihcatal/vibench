from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
import copy


@dataclass(slots=True)
class DocumentRecord:
    document_id: str
    partition_key: str
    body: dict[str, Any]
    etag: str | None = None
    updated_at: str | None = None


@dataclass(slots=True)
class QueryRequest:
    field_name: str
    field_value: Any
    partition_key: str | None = None
    limit: int = 25


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_document(
    document: dict[str, Any],
    document_id: str | None = None,
    partition_key: str | None = None,
) -> dict[str, Any]:
    normalized = copy.deepcopy(document)
    if document_id is not None:
        normalized["id"] = document_id
    if "id" not in normalized or not normalized["id"]:
        raise ValueError("document id is required")
    if partition_key is not None:
        normalized["partitionKey"] = partition_key
    normalized.setdefault("partitionKey", normalized["id"])
    normalized["updatedAt"] = utc_now_iso()
    normalized.setdefault("createdAt", normalized["updatedAt"])
    return normalized


def build_document_record(item: dict[str, Any]) -> DocumentRecord:
    return DocumentRecord(
        document_id=item["id"],
        partition_key=item.get("partitionKey", item["id"]),
        body=item,
        etag=item.get("_etag"),
        updated_at=item.get("updatedAt"),
    )


def coerce_text_fields(item: dict[str, Any], field_names: list[str]) -> dict[str, str]:
    values: dict[str, str] = {}
    for field_name in field_names:
        value = item.get(field_name)
        if value is None:
            continue
        values[field_name] = value if isinstance(value, str) else str(value)
    return values
