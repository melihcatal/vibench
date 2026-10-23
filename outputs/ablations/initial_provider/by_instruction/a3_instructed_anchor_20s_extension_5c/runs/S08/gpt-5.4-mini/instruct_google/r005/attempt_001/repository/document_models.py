from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    document_url: str = ""
    document_base64: str = ""
    mime_type: str = "application/pdf"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldConfidence:
    value: Any
    confidence: float = 0.0


@dataclass
class StructuredDocumentResponse:
    vendor: Optional[FieldConfidence] = None
    date: Optional[FieldConfidence] = None
    total: Optional[FieldConfidence] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    merchant: Optional[FieldConfidence] = None
    tax: Optional[FieldConfidence] = None
    items: List[Dict[str, Any]] = field(default_factory=list)


def normalize_extracted_fields(data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(data)
    if "total" in normalized and isinstance(normalized["total"], str):
        normalized["total"] = normalized["total"].replace(",", "")
    return normalized
