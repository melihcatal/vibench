from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class ExtractionRequest:
    source_uri: Optional[str] = None
    content: Optional[bytes] = None
    filename: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResponse:
    fields: Dict[str, Any] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)
    provider: str = ""


@dataclass
class NormalizedExpense:
    vendor: str
    date: Optional[str]
    total: Optional[float]
    currency: Optional[str] = None
    tax: Optional[float] = None
    items: List[Dict[str, Any]] = field(default_factory=list)
    invoice_number: Optional[str] = None
    confidence: Optional[float] = None

    def to_json(self) -> Dict[str, Any]:
        return {
            "vendor": self.vendor,
            "date": self.date,
            "total": self.total,
            "currency": self.currency,
            "tax": self.tax,
            "items": self.items,
            "invoice_number": self.invoice_number,
            "confidence": self.confidence,
        }
