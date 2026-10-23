from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentItem:
    description: str = ""
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None


@dataclass
class StructuredDocumentRequest:
    source_url: Optional[str] = None
    content: Optional[bytes] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredDocumentResponse:
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    items: List[DocumentItem] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Dict[str, float] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    provider: str
    document_type: str
    vendor: str
    date: str
    currency: str
    subtotal: Optional[float]
    tax: Optional[float]
    total: Optional[float]
    items: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None
    confidence: Dict[str, float] = field(default_factory=dict)


def normalize_money(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    text = str(value).strip().replace(",", "")
    if not text:
        return None
    try:
        return float(text)
    except ValueError:
        return None
