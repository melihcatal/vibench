from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    primary_key: str = "id"


@dataclass
class DocumentFetchRequest:
    identifier: Any
    primary_key: str = "id"


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    identifier: Any
    updates: Dict[str, Any]
    version_field: str = "version"
    expected_version: Optional[int] = None
    primary_key: str = "id"


@dataclass
class DocumentResponse:
    ok: bool
    data: Optional[Dict[str, Any]] = None
    items: Optional[List[Dict[str, Any]]] = None
    matched_count: int = 0
    modified_count: int = 0
    upserted_id: Optional[Any] = None
    error: Optional[str] = None


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(document)
    if "_id" in normalized and "id" not in normalized:
        normalized["id"] = str(normalized["_id"])
    return normalized
