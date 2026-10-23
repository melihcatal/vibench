from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


@dataclass
class DocumentExtractionRequest:
    document_text: str
    document_type: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionResponse:
    provider: str
    model: str
    extracted_at: datetime
    fields: Dict[str, Any]
    raw_response: Dict[str, Any]


@dataclass
class NormalizedExpense:
    vendor: str
    transaction_date: Optional[str]
    total: Optional[float]
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    tax: Optional[float] = None
    notes: Optional[str] = None


def normalize_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    for prefix in ("$", "USD "):
        text = text.replace(prefix, "")
    try:
        return float(text)
    except ValueError:
        return None


def normalize_date(value: Any) -> Optional[str]:
    if not value:
        return None
    if isinstance(value, str):
        return value[:10]
    if isinstance(value, datetime):
        return value.date().isoformat()
    return str(value)
