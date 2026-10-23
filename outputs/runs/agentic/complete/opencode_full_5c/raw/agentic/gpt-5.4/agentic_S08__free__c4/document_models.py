from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class DocumentSource:
    content: bytes
    mime_type: str
    filename: Optional[str] = None


@dataclass
class ExtractedField:
    value: Any
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "confidence": self.confidence}


@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractionResult:
    document_type: str
    provider: str
    fields: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "provider": self.provider,
            "fields": self.fields,
            "line_items": self.line_items,
            "raw_response": self.raw_response,
        }


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    vendor: Optional[str]
    merchant: Optional[str]
    document_date: Optional[str]
    currency: Optional[str]
    subtotal: Optional[float]
    tax: Optional[float]
    total: Optional[float]
    items: List[Dict[str, Any]]
    source_document_type: str
    provider: str
    confidence_summary: Dict[str, float]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def coerce_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).replace(",", "").strip()
    filtered = "".join(ch for ch in text if ch.isdigit() or ch in ".-")
    if not filtered:
        return None
    try:
        return float(filtered)
    except ValueError:
        return None


def normalize_confidence_map(fields: Dict[str, Dict[str, Any]]) -> Dict[str, float]:
    return {
        name: float(payload.get("confidence", 0.0) or 0.0)
        for name, payload in fields.items()
    }


def field_value(fields: Dict[str, Dict[str, Any]], key: str) -> Any:
    payload = fields.get(key, {})
    return payload.get("value")
