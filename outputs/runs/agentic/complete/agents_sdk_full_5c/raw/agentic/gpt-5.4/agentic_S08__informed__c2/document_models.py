from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class LineItem:
    description: Optional[str] = None
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
    raw_fields: Dict[str, Any] = field(default_factory=dict)
    provider: str = "azure-document-intelligence"
    average_confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        return payload


@dataclass
class NormalizedExpenseRecord:
    expense_id: str
    source_document_type: str
    supplier_name: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]]
    source_provider: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


REQUIRED_FIELDS = {
    "invoice": ["vendor", "invoice_date", "total"],
    "receipt": ["merchant", "total"],
}


def make_expense_id(prefix: str = "exp") -> str:
    return f"{prefix}_{uuid.uuid4().hex}"


def safe_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        stripped = value.replace(",", "").strip()
        if not stripped:
            return None
        try:
            return float(stripped)
        except ValueError:
            return None
    return None
