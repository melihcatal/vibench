from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class ExtractedLineItem:
    description: str
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
    line_items: List[ExtractedLineItem] = field(default_factory=list)
    items: List[ExtractedLineItem] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Dict[str, float] = field(default_factory=dict)
    raw_provider_response: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        payload["items"] = [item.to_dict() for item in self.items]
        return payload


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    source_document_type: str
    supplier_name: Optional[str]
    document_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    line_items: List[Dict[str, Any]]
    notes: Optional[str]
    validation: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def coerce_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").replace("$", "").strip()
        return float(cleaned)
    except (TypeError, ValueError):
        return None


def line_items_to_dicts(items: List[ExtractedLineItem]) -> List[Dict[str, Any]]:
    return [item.to_dict() for item in items]
