from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExtractionRequest:
    source_uri: Optional[str] = None
    content_type: str = "application/pdf"
    document_bytes: Optional[bytes] = None
    locale: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResponse:
    provider: str
    fields: Dict[str, Any]
    raw: Any = None
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {"provider": self.provider, "fields": self.fields, "raw": self.raw, "confidence": self.confidence}


@dataclass
class NormalizedExpense:
    vendor: str
    document_date: str
    total: float
    currency: str = "USD"
    items: List[Dict[str, Any]] = field(default_factory=list)
    tax: Optional[float] = None
    notes: Optional[str] = None
    source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def ensure_text(value: Any) -> str:
    return "" if value is None else str(value).strip()


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        if value is None:
            return default
        if isinstance(value, (int, float)):
            return float(value)
        text = str(value).replace(",", "").strip()
        return float(text)
    except (TypeError, ValueError):
        return default


def normalize_line_items(items: Any) -> List[Dict[str, Any]]:
    normalized: List[Dict[str, Any]] = []
    for item in items or []:
        if isinstance(item, dict):
            normalized.append({
                "description": ensure_text(item.get("description") or item.get("name")),
                "quantity": coerce_float(item.get("quantity"), 1.0),
                "unit_price": coerce_float(item.get("unit_price") or item.get("price")),
                "amount": coerce_float(item.get("amount") or item.get("total")),
            })
    return normalized
