from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class DocumentExtractionRequest:
    document_uri: str
    document_type: str
    locale: str = "en-US"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DocumentExtractionResponse:
    provider: str
    document_type: str
    fields: Dict[str, Any]
    confidences: Dict[str, float]
    raw_response: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    merchant: Optional[str] = None
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    items: List[Dict[str, Any]] = field(default_factory=list)
    notes: Optional[str] = None


def as_dict(record: NormalizedExpenseRecord) -> Dict[str, Any]:
    return {
        "merchant": record.merchant,
        "vendor": record.vendor,
        "date": record.date,
        "total": record.total,
        "tax": record.tax,
        "currency": record.currency,
        "items": record.items,
        "notes": record.notes,
    }
