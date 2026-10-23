from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class StructuredDocumentRequest:
    file_name: str
    content_type: str = "application/pdf"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StructuredDocumentField:
    name: str
    value: Any
    confidence: float = 0.0


@dataclass
class StructuredDocumentResponse:
    provider: str
    model_id: str
    fields: List[StructuredDocumentField] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class ExpenseNormalizationResult:
    vendor: str
    transaction_date: str
    total_amount: float
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    source_provider: str = "azure-document-intelligence"


REQUIRED_EXPENSE_FIELDS = ("vendor", "date", "total")


def field_map(fields: List[StructuredDocumentField]) -> Dict[str, StructuredDocumentField]:
    return {field.name: field for field in fields}


def normalize_currency(value: Optional[str]) -> str:
    if not value:
        return "USD"
    return str(value).upper()


def coerce_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
