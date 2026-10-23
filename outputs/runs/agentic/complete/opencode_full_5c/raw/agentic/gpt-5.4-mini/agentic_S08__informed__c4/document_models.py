import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    document_path: Optional[str] = None
    document_bytes: Optional[bytes] = None
    mime_type: Optional[str] = None
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredDocumentField:
    name: str
    value: Any
    confidence: Optional[float] = None
    page: Optional[int] = None
    normalized_value: Optional[Any] = None


@dataclass
class StructuredDocumentResponse:
    provider: str
    fields: Dict[str, StructuredDocumentField]
    raw: Dict[str, Any] = field(default_factory=dict)


def build_field(name: str, value: Any, confidence: Optional[float] = None, page: Optional[int] = None, normalized_value: Optional[Any] = None) -> StructuredDocumentField:
    return StructuredDocumentField(name=name, value=value, confidence=confidence, page=page, normalized_value=normalized_value)


def normalize_field_map(fields: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    normalized: Dict[str, Dict[str, Any]] = {}
    for key, value in fields.items():
        if isinstance(value, StructuredDocumentField):
            normalized[key] = {"value": value.value, "confidence": value.confidence, "page": value.page, "normalized_value": value.normalized_value}
        elif isinstance(value, dict):
            normalized[key] = value
        else:
            normalized[key] = {"value": value}
    return normalized
