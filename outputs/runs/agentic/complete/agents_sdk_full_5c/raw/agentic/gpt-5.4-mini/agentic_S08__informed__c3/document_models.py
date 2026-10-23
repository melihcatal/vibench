from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


@dataclass
class ExtractedDocument:
    document_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    notes: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)


@dataclass
class NormalizedExpense:
    source_type: str
    counterparty: Optional[str]
    transaction_date: Optional[str]
    total_amount: Optional[float]
    tax_amount: Optional[float]
    currency: Optional[str]
    line_items: List[Dict[str, Any]]
    memo: Optional[str] = None


def as_json_dict(obj: Any) -> Dict[str, Any]:
    if hasattr(obj, "__dict__"):
        return {k: v for k, v in obj.__dict__.items() if v is not None}
    return dict(obj)
