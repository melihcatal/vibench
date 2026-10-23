from dataclasses import dataclass, field
from typing import Any, Dict, Optional


def normalize_document(document):
    if document is None:
        return None
    if isinstance(document, dict):
        return document
    return dict(document)


@dataclass
class DocumentKey:
    document_id: str
    category: Optional[str] = None

    def as_item(self):
        item = {"document_id": self.document_id}
        if self.category is not None:
            item["category"] = self.category
        return item


@dataclass
class UpsertDocumentRequest:
    document: Dict[str, Any]
    return_values: str = "ALL_NEW"


@dataclass
class FetchDocumentRequest:
    document_id: str
    category: Optional[str] = None


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any] = field(default_factory=dict)
    expected_version: Optional[int] = None
    category: Optional[str] = None


@dataclass
class DocumentResponse:
    ok: bool
    data: Dict[str, Any]
