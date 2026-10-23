from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


@dataclass
class UpsertDocumentRequest:
    id: str
    document: Dict[str, Any] = field(default_factory=dict)

    def to_item(self) -> Dict[str, Any]:
        item = dict(self.document)
        item["id"] = self.id
        return normalize_document(item)


@dataclass
class FetchDocumentResponse:
    found: bool
    document: Optional[Dict[str, Any]] = None


@dataclass
class QueryDocumentsRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    id: str
    etag: Optional[str] = None
    version: Optional[int] = None
    patch: Dict[str, Any] = field(default_factory=dict)


def merge_document(current: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(current)
    merged.update(normalize_document(patch))
    return merged
