from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return dict(document or {})


def normalize_query_value(value: Any) -> Any:
    return value.strip() if isinstance(value, str) else value


@dataclass
class DocumentResponse:
    document: Optional[Dict[str, Any]]
    found: bool


@dataclass
class QueryResponse:
    documents: List[Dict[str, Any]]


@dataclass
class UpdateRequest:
    document_id: str
    changes: Dict[str, Any]
    etag: Optional[str] = None


def normalize_documents(documents: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_document(item) for item in documents]
