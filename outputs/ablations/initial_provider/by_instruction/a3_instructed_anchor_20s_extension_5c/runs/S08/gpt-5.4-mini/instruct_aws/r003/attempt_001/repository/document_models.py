from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentExtractionRequest:
    document_uri: Optional[str] = None
    document_bytes: Optional[bytes] = None
    mime_type: str = "application/pdf"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionResponse:
    provider: str
    fields: Dict[str, Any]
    confidence: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_field_list(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    normalized = {}
    for item in items:
        name = item.get("name") or item.get("field")
        if name:
            normalized[name] = item.get("value")
    return normalized
