from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0
    unit: Optional[str] = None
    currency: Optional[str] = None


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: float = 0.0


@dataclass
class DocumentExtractionRequest:
    document_uri: Optional[str] = None
    content_type: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionResponse:
    provider: str
    fields: Dict[str, DocumentField] = field(default_factory=dict)
    line_items: List[LineItem] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    source: str
    vendor: str
    date: Optional[str]
    total: Optional[float]
    currency: Optional[str]
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0


def field_to_dict(field: DocumentField) -> Dict[str, Any]:
    return {
        "name": field.name,
        "value": field.value,
        "confidence": field.confidence,
        "unit": field.unit,
        "currency": field.currency,
    }


def normalized_expense_to_dict(record: NormalizedExpenseRecord) -> Dict[str, Any]:
    return {
        "source": record.source,
        "vendor": record.vendor,
        "date": record.date,
        "total": record.total,
        "currency": record.currency,
        "line_items": record.line_items,
        "confidence": record.confidence,
    }
