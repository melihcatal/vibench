from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class StructuredDocumentExtractionRequest:
    content: bytes
    filename: Optional[str] = None
    content_type: str = "application/pdf"


@dataclass
class StructuredDocumentExtractionResponse:
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    merchant: Optional[str] = None
    notes: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    items: List[Dict[str, Any]] = field(default_factory=list)
    confidence: Optional[float] = None
    raw: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedExpenseRecord:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    currency: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    source_confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "vendor": self.vendor,
            "merchant": self.merchant,
            "date": self.date,
            "currency": self.currency,
            "total": self.total,
            "tax": self.tax,
            "line_items": self.line_items,
            "source_confidence": self.source_confidence,
            "metadata": self.metadata,
        }


def normalize_line_item(item: Any) -> Dict[str, Any]:
    if isinstance(item, LineItem):
        return {
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "amount": item.amount,
            "confidence": item.confidence,
        }
    if isinstance(item, dict):
        return item
    return {"description": str(item)}
