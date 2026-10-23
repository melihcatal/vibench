from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from decimal import Decimal, InvalidOperation
from typing import Any, Dict, List, Optional
import uuid


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
    tax: Optional[float] = None
    total: Optional[float] = None
    currency: Optional[str] = None
    vendor_notes: Optional[str] = None
    notes: Optional[str] = None
    raw_fields: Dict[str, Any] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    items: List[LineItem] = field(default_factory=list)
    confidence: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        payload["items"] = [item.to_dict() for item in self.items]
        return payload


@dataclass
class NormalizedExpense:
    record_id: str
    source_type: str
    supplier_name: str
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    memo: Optional[str]
    items: List[Dict[str, Any]]
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
        return float(Decimal(str(value).replace(",", "")))
    except (InvalidOperation, ValueError):
        return None



def iso_date_or_none(value: Any) -> Optional[str]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    text = str(value).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return text



def new_record_id(prefix: str = "exp") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"
