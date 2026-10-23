from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, MutableMapping, Optional


@dataclass
class DocumentRequest:
    document: Dict[str, Any]
    db_name: Optional[str] = None
    collection_name: Optional[str] = None


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any
    db_name: Optional[str] = None
    collection_name: Optional[str] = None
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    document_id: Any
    expected_version: Optional[int] = None
    update_fields: Dict[str, Any] = field(default_factory=dict)
    db_name: Optional[str] = None
    collection_name: Optional[str] = None


@dataclass
class OperationResponse:
    ok: bool
    provider: str
    data: Dict[str, Any] = field(default_factory=dict)


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "_id" not in normalized:
        for key in ("id", "document_id", "record_id"):
            if key in normalized:
                normalized["_id"] = normalized[key]
                break
    if "_id" in normalized:
        normalized["_id"] = str(normalized["_id"])
    return normalized


def normalize_for_update(fields: MutableMapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(fields)
    normalized.pop("_id", None)
    normalized.pop("id", None)
    normalized.pop("document_id", None)
    normalized.pop("record_id", None)
    return normalized
