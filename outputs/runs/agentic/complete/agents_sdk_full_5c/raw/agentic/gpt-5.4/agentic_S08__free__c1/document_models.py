from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class ExtractedDocument:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    invoice_date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    notes: Optional[str] = None
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    record_type: str
    supplier_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    line_items: List[Dict[str, Any]]
    source_document_type: str
    source_notes: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def parse_float(value: Any) -> Optional[float]:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        cleaned = str(value).replace(",", "").replace("$", "").strip()
        return float(Decimal(cleaned))
    except (InvalidOperation, ValueError):
        return None


def normalize_date(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            continue
    return value


def line_item_to_dict(item: LineItem) -> Dict[str, Any]:
    return asdict(item)


def line_items_from_any(items: Any) -> List[LineItem]:
    results: List[LineItem] = []
    if not isinstance(items, list):
        return results
    for item in items:
        if isinstance(item, LineItem):
            results.append(item)
            continue
        if isinstance(item, dict):
            results.append(
                LineItem(
                    description=str(item.get("description") or item.get("name") or ""),
                    quantity=parse_float(item.get("quantity")),
                    unit_price=parse_float(item.get("unit_price") or item.get("price")),
                    amount=parse_float(item.get("amount") or item.get("total_price")),
                    confidence=parse_float(item.get("confidence")),
                )
            )
    return results
