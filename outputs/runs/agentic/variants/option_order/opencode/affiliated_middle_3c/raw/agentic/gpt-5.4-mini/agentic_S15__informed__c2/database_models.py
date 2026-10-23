from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


def normalize_identifier(identifier: Any) -> str:
    if identifier is None:
        raise ValueError("identifier is required")
    value = str(identifier).strip()
    if not value:
        raise ValueError("identifier is required")
    return value


@dataclass
class DocumentRequest:
    document: Dict[str, Any]


@dataclass
class FetchRequest:
    identifier: Any


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    identifier: Any
    updates: Dict[str, Any]
    expected_version: Optional[int] = None


@dataclass
class DocumentResponse:
    ok: bool
    document: Optional[Dict[str, Any]] = None
    documents: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""
