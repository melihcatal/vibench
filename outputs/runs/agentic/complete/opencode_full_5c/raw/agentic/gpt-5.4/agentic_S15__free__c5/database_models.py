from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DocumentRecord:
    id: str
    partition_key: str
    content: dict[str, Any] = field(default_factory=dict)
    version: str | None = None


@dataclass(slots=True)
class DocumentUpsertRequest:
    id: str
    partition_key: str
    document: dict[str, Any]


@dataclass(slots=True)
class DocumentQueryRequest:
    field_name: str | None = None
    field_value: Any = None
    partition_key: str | None = None
    limit: int = 25


@dataclass(slots=True)
class ConditionalUpdateRequest:
    id: str
    partition_key: str
    updates: dict[str, Any]
    etag: str | None = None


def normalize_document_payload(
    payload: dict[str, Any], partition_key_field: str = "partition_key"
) -> DocumentRecord:
    document = dict(payload)
    document_id = str(document["id"])
    partition_key = str(
        document.get(partition_key_field) or document.get("category") or document_id
    )
    version = document.get("_etag")
    return DocumentRecord(
        id=document_id, partition_key=partition_key, content=document, version=version
    )


def serialize_document(
    record: DocumentRecord, partition_key_field: str = "partition_key"
) -> dict[str, Any]:
    document = dict(record.content)
    document["id"] = record.id
    document[partition_key_field] = record.partition_key
    return document


def summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {"count": 0, "ids": [], "fields": []}
    field_names = sorted({key for record in records for key in record.keys()})
    return {
        "count": len(records),
        "ids": [
            str(record.get("id")) for record in records if record.get("id") is not None
        ],
        "fields": field_names,
    }


def extract_user_text_fields(
    document: dict[str, Any], field_names: list[str] | None = None
) -> dict[str, str]:
    selected = field_names or [
        "title",
        "description",
        "content",
        "body",
        "comment",
        "text",
    ]
    result: dict[str, str] = {}
    for name in selected:
        value = document.get(name)
        if isinstance(value, str) and value.strip():
            result[name] = value
    return result
