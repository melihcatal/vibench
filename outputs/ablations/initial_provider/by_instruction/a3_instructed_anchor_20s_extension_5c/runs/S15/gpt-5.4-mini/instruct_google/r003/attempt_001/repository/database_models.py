from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_document(document: Any) -> Dict[str, Any]:
    if document is None:
        return {}
    if isinstance(document, dict):
        return document
    raise TypeError("document must be a mapping")


@dataclass
class DocumentKey:
    document_id: str


@dataclass
class UpsertDocumentRequest:
    collection: str
    document: Dict[str, Any]
    document_id_field: str = "id"


@dataclass
class FetchDocumentRequest:
    collection: str
    document_id: str


@dataclass
class QueryDocumentsRequest:
    collection: str
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
