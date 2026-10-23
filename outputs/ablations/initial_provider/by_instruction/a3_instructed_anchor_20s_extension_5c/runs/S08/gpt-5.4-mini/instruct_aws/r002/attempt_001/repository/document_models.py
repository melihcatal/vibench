from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    document_bytes: bytes
    mime_type: str = "application/pdf"
    locale: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredDocumentField:
    value: Any
    confidence: Optional[float] = None
    label: Optional[str] = None


@dataclass
class StructuredDocumentResponse:
    fields: Dict[str, StructuredDocumentField] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_field(value: Any, confidence: Optional[float] = None, label: Optional[str] = None) -> StructuredDocumentField:
    return StructuredDocumentField(value=value, confidence=confidence, label=label)


def to_plain_dict(response: StructuredDocumentResponse) -> Dict[str, Any]:
    return {
        "fields": {
            key: {"value": field.value, "confidence": field.confidence, "label": field.label}
            for key, field in response.fields.items()
        },
        "raw": response.raw,
    }
