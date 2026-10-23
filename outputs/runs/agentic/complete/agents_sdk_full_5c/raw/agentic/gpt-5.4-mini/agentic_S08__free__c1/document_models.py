from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    document_id: str
    content: str
    document_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentResponse:
    document_id: str
    fields: Dict[str, Any]
    confidence: float = 0.0
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    vendor: str
    date: str
    total: float
    currency: str = "USD"
    items: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None


def coerce_confidence(value: Any) -> float:
    try:
        confidence = float(value)
    except (TypeError, ValueError):
        confidence = 0.0
    return max(0.0, min(1.0, confidence))
