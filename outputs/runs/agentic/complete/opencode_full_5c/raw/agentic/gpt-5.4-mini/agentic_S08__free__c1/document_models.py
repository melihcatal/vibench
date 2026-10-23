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
    provider: str
    fields: List[DocumentField] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    vendor: Optional[str]
    date: Optional[str]
    total: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0


def normalize_currency_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    for prefix in ("$", "€", "£"):
        text = text.replace(prefix, "")
    try:
        return float(text)
    except ValueError:
        return None


def fields_to_dict(fields: List[DocumentField]) -> Dict[str, Any]:
    return {
        field.name: {"value": field.value, "confidence": field.confidence}
        for field in fields
    }
