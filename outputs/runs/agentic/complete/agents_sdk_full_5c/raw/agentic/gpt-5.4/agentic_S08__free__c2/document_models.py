from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractedField:
    value: Any
    confidence: Optional[float] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentExtractionResult:
    document_type: str
    vendor: Optional[ExtractedField] = None
    merchant: Optional[ExtractedField] = None
    date: Optional[ExtractedField] = None
    tax: Optional[ExtractedField] = None
    total: Optional[ExtractedField] = None
    currency: Optional[ExtractedField] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "document_type": self.document_type,
            "vendor": self.vendor.to_dict() if self.vendor else None,
            "merchant": self.merchant.to_dict() if self.merchant else None,
            "date": self.date.to_dict() if self.date else None,
            "tax": self.tax.to_dict() if self.tax else None,
            "total": self.total.to_dict() if self.total else None,
            "currency": self.currency.to_dict() if self.currency else None,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_response": self.raw_response,
        }
        return data


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    supplier_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]]
    source_document_type: str
    validation_status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationIssue:
    field: str
    message: str
    severity: str = "error"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def coerce_float(value: Any) -> Optional[float]:
    if value is None:
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


def normalize_items(items: List[Any]) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        if isinstance(item, LineItem):
            normalized.append(item.to_dict())
        elif isinstance(item, dict):
            normalized.append(
                {
                    "description": item.get("description") or item.get("name"),
                    "quantity": coerce_float(item.get("quantity")),
                    "unit_price": coerce_float(item.get("unit_price")),
                    "amount": coerce_float(item.get("amount") or item.get("total_price")),
                    "confidence": item.get("confidence"),
                }
            )
    return normalized
