from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str = ""
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractedDocument:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    invoice_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Dict[str, float] = field(default_factory=dict)
    raw_provider_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        return payload


@dataclass
class NormalizedExpenseRecord:
    record_type: str = "expense"
    source_document_type: str = ""
    counterparty_name: Optional[str] = None
    document_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    items: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None
    validation_status: str = "unvalidated"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def coerce_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(Decimal(str(value).replace(",", "").strip()))
    except (InvalidOperation, ValueError):
        return None


def normalize_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y", "%m-%d-%Y"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value


def normalize_line_item(item: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "description": item.get("description") or item.get("product_code") or "",
        "quantity": coerce_float(item.get("quantity")),
        "unit_price": coerce_float(item.get("unit_price")),
        "amount": coerce_float(item.get("amount") or item.get("total_price")),
        "confidence": coerce_float(item.get("confidence")),
    }
