from dataclasses import dataclass, field
from typing import Any, Dict, Optional, List


@dataclass
class Document:
    id: str
    data: Dict[str, Any]
    version: Optional[int] = None


@dataclass
class QueryFilter:
    field: str
    value: Any


@dataclass
class DocumentSummary:
    id: str
    summary_text: str


@dataclass
class SafetyResult:
    id: str
    is_safe: bool
    scores: Dict[str, Any]


@dataclass
class TranslatedDocument:
    id: str
    translated_fields: Dict[str, str]
    target_language: str
