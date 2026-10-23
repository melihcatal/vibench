from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_identifier(value: Any) -> str:
    return str(value)


def normalize_document_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    if "id" in normalized:
        normalized["id"] = normalize_identifier(normalized["id"])
    if "partition_key" in normalized:
        normalized["partition_key"] = normalize_identifier(normalized["partition_key"])
    return normalized


@dataclass
class UpsertDocumentRequest:
    document: Dict[str, Any]


@dataclass
class FetchDocumentRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_etag: Optional[str] = None
    partition_key: Optional[str] = None


@dataclass
class ServiceResponse:
    ok: bool
    data: Dict[str, Any]
