from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


def extract_document_id(document: Dict[str, Any], id_field: str = "id") -> str:
    value = document.get(id_field)
    if value is None:
        raise ValueError(f"missing required id field: {id_field}")
    return str(value)


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    id_field: str = "id"


@dataclass
class DocumentFetchRequest:
    document_id: str


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    version_field: str = "version"


@dataclass
class DocumentResponse:
    document: Optional[Dict[str, Any]] = None
    documents: List[Dict[str, Any]] = field(default_factory=list)
    matched_count: int = 0
    modified_count: int = 0
