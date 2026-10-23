from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional


@dataclass
class ExtractedField:
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
        return asdict(self)


@dataclass
class DocumentExtractionResult:
    document_type: str
    provider: str
    vendor: Optional[ExtractedField] = None
    merchant: Optional[ExtractedField] = None
    date: Optional[ExtractedField] = None
    tax: Optional[ExtractedField] = None
    total: Optional[ExtractedField] = None
    currency: Optional[ExtractedField] = None
    notes: Optional[ExtractedField] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "document_type": self.document_type,
            "provider": self.provider,
            "vendor": self.vendor.to_dict() if self.vendor else None,
            "merchant": self.merchant.to_dict() if self.merchant else None,
            "date": self.date.to_dict() if self.date else None,
            "tax": self.tax.to_dict() if self.tax else None,
            "total": self.total.to_dict() if self.total else None,
            "currency": self.currency.to_dict() if self.currency else None,
            "notes": self.notes.to_dict() if self.notes else None,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_response": self.raw_response,
        }
        return payload


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    source_document_type: str
    supplier_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]]
    notes: Optional[str]
    validation_errors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


REQUIRED_FIELDS_BY_TYPE = {
    "invoice": ["vendor", "date", "total"],
    "receipt": ["merchant", "total"],
}


def coerce_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, str):
        cleaned = value.replace("$", "").replace(",", "").strip()
        if not cleaned:
            return None
        return float(cleaned)
    raise TypeError(f"Unsupported numeric value: {type(value)!r}")



def normalize_date(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, str):
        text = value.strip()
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(text, fmt).date().isoformat()
            except ValueError:
                continue
        return text
    return str(value)
