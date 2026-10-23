from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    partition_key: Optional[str] = None


@dataclass
class DocumentFetchRequest:
    document_id: str
    partition_key: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    partition_key: Optional[str] = None
    limit: int = 20


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    expected_version: Optional[int]
    updates: Dict[str, Any]
    partition_key: Optional[str] = None


@dataclass
class DocumentOperationResponse:
    ok: bool
    document: Dict[str, Any]
    matched_count: int = 0
    modified_count: int = 0
    message: str = ""


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "id" not in normalized and "document_id" in normalized:
        normalized["id"] = str(normalized["document_id"])
    if "id" in normalized:
        normalized["id"] = str(normalized["id"])
    if "partition_key" in normalized and normalized["partition_key"] is not None:
        normalized["partition_key"] = str(normalized["partition_key"])
    return normalized


def coerce_list(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_document(item) for item in items]
