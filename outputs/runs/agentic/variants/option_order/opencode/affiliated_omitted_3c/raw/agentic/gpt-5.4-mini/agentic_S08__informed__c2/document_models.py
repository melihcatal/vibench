from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    content: Optional[bytes] = None
    mime_type: str = "application/pdf"


@dataclass
class DocumentField:
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentResponse:
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpense:
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    items: List[Dict[str, Any]] = field(default_factory=list)


def as_field(value: Any, confidence: float = 0.0) -> DocumentField:
    return DocumentField(value=value, confidence=confidence)


def expense_to_json(expense: NormalizedExpense) -> Dict[str, Any]:
    return {
        "vendor": expense.vendor,
        "date": expense.date,
        "total": expense.total,
        "tax": expense.tax,
        "currency": expense.currency,
        "items": expense.items,
    }
