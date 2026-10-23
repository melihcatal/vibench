from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_identifier(value: Any) -> str:
    if value is None:
        raise ValueError("identifier is required")
    text = str(value).strip()
    if not text:
        raise ValueError("identifier is required")
    return text


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(document, dict):
        raise TypeError("document must be a mapping")
    return dict(document)


@dataclass
class DocumentUpsertRequest:
    document: Dict[str, Any]
    primary_key: str = "id"


@dataclass
class DocumentFetchRequest:
    document_id: Any
    partition_key: Optional[Any] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    document_id: Any
    updates: Dict[str, Any]
    etag: Optional[str] = None
    version_field: str = "version"


@dataclass
class DocumentResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    documents: List[Dict[str, Any]] = field(default_factory=list)
    etag: Optional[str] = None
    error: Optional[str] = None
