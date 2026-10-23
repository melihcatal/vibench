from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Iterable, List, Optional


def _normalize_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_normalize_value(v) for v in value]
    if isinstance(value, tuple):
        return [_normalize_value(v) for v in value]
    return value


@dataclass
class DocumentRequest:
    collection: str
    document_id: str
    data: Dict[str, Any] = field(default_factory=dict)

    def normalized_payload(self) -> Dict[str, Any]:
        payload = dict(self.data)
        payload["id"] = self.document_id
        return _normalize_value(payload)


@dataclass
class QueryRequest:
    collection: str
    field_name: str
    field_value: Any
    limit: int = 50


@dataclass
class ConditionalUpdateRequest:
    collection: str
    document_id: str
    expected_version: int
    patch: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    document_id: str
    data: Dict[str, Any]
    found: bool = True
    etag: Optional[str] = None

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueryResponse:
    items: List[Dict[str, Any]]
    count: int

    def as_dict(self) -> Dict[str, Any]:
        return {"items": self.items, "count": self.count}


@dataclass
class ArchiveRequest:
    bucket: str
    object_name: str
    payload: bytes
    content_type: str = "application/octet-stream"


@dataclass
class SafetyFinding:
    label: str
    score: float
    unsafe: bool = False


@dataclass
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass
class SummaryResponse:
    title: str
    summary: str
    metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_document(document: Dict[str, Any]) -> Dict[str, Any]:
    return _normalize_value(document)


def extract_text_fields(document: Dict[str, Any], fields: Iterable[str]) -> Dict[str, str]:
    extracted: Dict[str, str] = {}
    for field_name in fields:
        value = document.get(field_name)
        if value is not None:
            extracted[field_name] = str(value)
    return extracted
