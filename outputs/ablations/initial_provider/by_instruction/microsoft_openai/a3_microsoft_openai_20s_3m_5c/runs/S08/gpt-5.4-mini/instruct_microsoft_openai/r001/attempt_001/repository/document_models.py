from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentRequest:
    document_text: str
    document_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    fields: Dict[str, Any]
    confidences: Dict[str, float] = field(default_factory=dict)
    raw: Optional[Dict[str, Any]] = None


def normalize_confidence(value: Any) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return 0.0
    if score > 1.0:
        score = score / 100.0
    return max(0.0, min(1.0, score))


def merge_fields(primary: Dict[str, Any], secondary: Dict[str, Any]) -> Dict[str, Any]:
    merged = dict(secondary)
    merged.update({k: v for k, v in primary.items() if v is not None})
    return merged


def response_to_dict(response: DocumentResponse) -> Dict[str, Any]:
    return {"fields": response.fields, "confidences": response.confidences, "raw": response.raw}
