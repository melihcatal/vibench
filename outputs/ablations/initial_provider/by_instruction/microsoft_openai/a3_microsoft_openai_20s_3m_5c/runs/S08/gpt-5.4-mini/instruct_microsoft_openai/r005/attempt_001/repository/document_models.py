from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_text: str
    document_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentResponse:
    document_type: str
    fields: List[DocumentField] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = 0.0
    if confidence < 0.0:
        return 0.0
    if confidence > 1.0:
        return 1.0
    return confidence


def response_from_dict(data: Dict[str, Any], document_type: str) -> DocumentResponse:
    fields = []
    for item in data.get("fields", []):
        fields.append(DocumentField(name=item.get("name", ""), value=item.get("value"), confidence=normalize_confidence(item.get("confidence", 0.0))))
    return DocumentResponse(document_type=document_type, fields=fields, raw=data)
