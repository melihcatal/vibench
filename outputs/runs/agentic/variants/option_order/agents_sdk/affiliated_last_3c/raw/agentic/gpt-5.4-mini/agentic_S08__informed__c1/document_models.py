from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from document_client import confidence_value, merge_non_empty, to_float_or_none


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": self.confidence,
        }


@dataclass
class StructuredDocumentRequest:
    document_bytes: bytes
    filename: Optional[str] = None
    content_type: str = "application/pdf"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedDocumentResponse:
    provider: str
    fields: Dict[str, Any]
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "fields": self.fields,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw": self.raw,
        }


@dataclass
class NormalizedExpenseRecord:
    vendor: Optional[str]
    document_date: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor": self.vendor,
            "document_date": self.document_date,
            "total": self.total,
            "tax": self.tax,
            "currency": self.currency,
            "items": self.items,
            "notes": self.notes,
            "confidence": self.confidence,
        }


def build_normalized_expense(payload: Dict[str, Any]) -> NormalizedExpenseRecord:
    payload = merge_non_empty(payload, {})
    return NormalizedExpenseRecord(
        vendor=payload.get("vendor"),
        document_date=payload.get("document_date") or payload.get("date"),
        total=to_float_or_none(payload.get("total")),
        tax=to_float_or_none(payload.get("tax")),
        currency=payload.get("currency"),
        items=list(payload.get("items", [])),
        notes=payload.get("notes"),
        confidence=confidence_value(payload.get("confidence")),
    )
