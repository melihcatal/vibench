from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Any, Dict, List, Optional


@dataclass
class DocumentLineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DocumentExtractionRequest:
    file_path: str
    content_type: str = "application/pdf"
    processor_id: Optional[str] = None
    mime_type: Optional[str] = None


@dataclass
class DocumentExtractionResponse:
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[DocumentLineItem] = field(default_factory=list)
    confidence: Optional[float] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = asdict(self)
        payload["line_items"] = [item.to_dict() for item in self.line_items]
        return payload


@dataclass
class NormalizedExpenseRecord:
    source: str
    vendor: Optional[str]
    transaction_date: Optional[str]
    total: Optional[float]
    tax: Optional[float]
    currency: Optional[str]
    items: List[Dict[str, Any]]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ValidationResult:
    valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
