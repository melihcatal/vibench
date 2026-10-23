from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExtractionField:
    value: Any
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"value": self.value, "confidence": self.confidence}


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total": self.total,
            "confidence": self.confidence,
        }


@dataclass
class DocumentExtractionResult:
    document_type: str
    fields: Dict[str, ExtractionField] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "fields": {key: field.to_dict() for key, field in self.fields.items()},
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_response": self.raw_response,
        }


@dataclass
class NormalizedExpenseRecord:
    source_document_type: str
    vendor: Optional[str]
    merchant: Optional[str]
    document_date: Optional[str]
    currency: Optional[str]
    subtotal: Optional[float]
    tax: Optional[float]
    total: Optional[float]
    items: List[Dict[str, Any]]
    notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_document_type": self.source_document_type,
            "vendor": self.vendor,
            "merchant": self.merchant,
            "document_date": self.document_date,
            "currency": self.currency,
            "subtotal": self.subtotal,
            "tax": self.tax,
            "total": self.total,
            "items": self.items,
            "notes": self.notes,
            "metadata": self.metadata,
        }


def safe_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace(",", "").replace("$", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def as_confidence(value: Any) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0
    return max(0.0, min(parsed, 1.0))


def compact_dict(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}
