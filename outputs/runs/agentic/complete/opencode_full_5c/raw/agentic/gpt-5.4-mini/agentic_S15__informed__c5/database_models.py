from dataclasses import dataclass
from typing import Any


def normalize_document(document: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(document)
    if "id" not in normalized and "_id" in normalized:
        normalized["id"] = str(normalized.pop("_id"))
    if "version" in normalized and normalized["version"] is not None:
        normalized["version"] = int(normalized["version"])
    return normalized


@dataclass(frozen=True)
class DocumentUpsertRequest:
    document: dict[str, Any]


@dataclass(frozen=True)
class DocumentFetchRequest:
    document_id: str


@dataclass(frozen=True)
class DocumentQueryRequest:
    field_name: str
    field_value: Any


@dataclass(frozen=True)
class ConditionalUpdateRequest:
    document_id: str
    patch: dict[str, Any]
    expected_version: int | None = None
