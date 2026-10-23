from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0


@dataclass
class DocumentExtractionResult:
    provider: str
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExpenseRecord:
    vendor: str
    document_date: Optional[str]
    total: float
    currency: str = "USD"
    tax: Optional[float] = None
    items: List[Dict[str, Any]] = field(default_factory=list)
    source_provider: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    score: float = 0.0


def normalize_amount(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        cleaned = "".join(ch for ch in value if ch.isdigit() or ch in ".-")
        if cleaned in {"", ".", "-", "-."}:
            return None
        try:
            return float(cleaned)
        except ValueError:
            return None
    return None


def normalize_text(value: Any) -> str:
    return "" if value is None else str(value).strip()
