from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalize_value(value: Any) -> Any:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc).isoformat()
    if isinstance(value, dict):
        return {str(k): _normalize_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize_value(v) for v in value]
    return value


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    return {str(k): _normalize_value(v) for k, v in document.items()}


def ensure_primary_id(document: Mapping[str, Any], primary_key: str = "id") -> str:
    value = document.get(primary_key)
    if value is None:
        raise ValueError(f"missing primary key field: {primary_key}")
    return str(value)


@dataclass(slots=True)
class DocumentRequest:
    document: Dict[str, Any]
    primary_key: str = "id"

    def normalized(self) -> Dict[str, Any]:
        data = normalize_document(self.document)
        data.setdefault(self.primary_key, ensure_primary_id(data, self.primary_key))
        return data


@dataclass(slots=True)
class QueryRequest:
    field_name: str
    field_value: Any
    limit: int = 50


@dataclass(slots=True)
class UpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    primary_key: str = "id"


@dataclass(slots=True)
class DocumentResponse:
    document: Dict[str, Any]
    source: str = "amazon-dynamodb"
    fetched_at: str = field(default_factory=_utc_now_iso)

    def as_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class QueryResponse:
    documents: List[Dict[str, Any]]
    source: str = "amazon-dynamodb"
    count: int = 0

    def __post_init__(self) -> None:
        self.count = len(self.documents)


@dataclass(slots=True)
class UpdateResponse:
    document: Dict[str, Any]
    updated: bool = True
    source: str = "amazon-dynamodb"


@dataclass(slots=True)
class ArchiveRequest:
    bucket: str
    object_key: str
    body: bytes
    content_type: str = "application/json"


@dataclass(slots=True)
class SafetyFinding:
    field: str
    unsafe: bool
    reason: str = ""


@dataclass(slots=True)
class SafetyResponse:
    findings: List[SafetyFinding]
    unsafe: bool = False

    def __post_init__(self) -> None:
        self.unsafe = any(f.unsafe for f in self.findings)


@dataclass(slots=True)
class TranslationRequest:
    text: str
    target_language: str
    source_language: Optional[str] = None


@dataclass(slots=True)
class TranslationResponse:
    translated_text: str
    source_language: Optional[str] = None
    target_language: Optional[str] = None
