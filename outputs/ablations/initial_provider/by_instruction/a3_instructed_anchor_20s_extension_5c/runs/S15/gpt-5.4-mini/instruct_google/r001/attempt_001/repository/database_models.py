from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if document is None:
        return {}
    if not isinstance(document, dict):
        raise TypeError("document must be a mapping")
    return {k: v for k, v in document.items() if v is not None}


@dataclass
class DocumentKey:
    document_id: str


@dataclass
class UpsertRequest:
    collection: str
    document: Dict[str, Any]
    document_id_field: str = "id"


@dataclass
class FetchRequest:
    collection: str
    document_id: str
    document_id_field: str = "id"


@dataclass
class QueryRequest:
    collection: str
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    version_field: str = "version"


@dataclass
class OperationResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    documents: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
