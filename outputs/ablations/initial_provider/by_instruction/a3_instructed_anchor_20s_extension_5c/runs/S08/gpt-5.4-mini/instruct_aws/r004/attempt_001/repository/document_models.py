from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_uri: Optional[str] = None
    document_bytes: Optional[bytes] = None
    mime_type: str = "application/pdf"
    fields: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FieldValue:
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None


@dataclass
class DocumentResponse:
    fields: Dict[str, FieldValue] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


def as_jsonable_response(response: DocumentResponse) -> Dict[str, Any]:
    return {
        "fields": {
            key: {
                "value": item.value,
                "confidence": item.confidence,
                "source": item.source,
            }
            for key, item in response.fields.items()
        },
        "raw": response.raw,
    }


def normalize_field_name(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace("-", "_")
