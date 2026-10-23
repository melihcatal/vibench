from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, MutableMapping, Optional


def normalize_document(document: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in document.items() if v is not None}


@dataclass
class DocumentUpsertRequest:
    document_id: str
    document: Dict[str, Any]
    table_name: Optional[str] = None


@dataclass
class DocumentFetchRequest:
    document_id: str
    table_name: Optional[str] = None


@dataclass
class DocumentQueryRequest:
    field_name: str
    field_value: Any
    table_name: Optional[str] = None
    limit: Optional[int] = None


@dataclass
class DocumentConditionalUpdateRequest:
    document_id: str
    updates: Dict[str, Any]
    expected_version: Optional[int] = None
    table_name: Optional[str] = None


@dataclass
class OperationResponse:
    ok: bool
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None


@dataclass
class RecordSummary:
    document_id: str
    title: str
    summary: str


@dataclass
class SafetyResult:
    document_id: str
    is_safe: bool
    reasons: List[str] = field(default_factory=list)


@dataclass
class TranslationResult:
    document_id: str
    translated_fields: Dict[str, Any]
    target_language: str


@dataclass
class ExportArchiveResult:
    document_id: str
    bucket: str
    key: str
    url: str
