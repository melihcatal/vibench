from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_id: str
    payload: Dict[str, Any] = field(default_factory=dict)


@dataclass
class QueryRequest:
    field_name: str
    field_value: Any


@dataclass
class ConditionalUpdateRequest:
    document_id: str
    expected_version: int
    updates: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    found: bool
    document: Optional[Dict[str, Any]] = None
    matched_count: int = 0
    modified_count: int = 0
    version: Optional[int] = None


@dataclass
class QueryResponse:
    documents: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SummaryResponse:
    summary: str
    document_count: int
