from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    file_path: str
    mime_type: str = "application/pdf"
    document_bytes: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class StructuredDocumentResponse:
    provider: str
    fields: List[StructuredField] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_field_map(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {str(k).lower().replace(" ", "_"): v for k, v in payload.items()}


def response_to_schema(response: StructuredDocumentResponse) -> Dict[str, Any]:
    return {
        "provider": response.provider,
        "fields": [
            {"name": f.name, "value": f.value, "confidence": f.confidence}
            for f in response.fields
        ],
        "raw": response.raw,
    }
