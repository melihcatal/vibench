from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class ExtractedField:
    value: str
    confidence: float


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None
    confidence: float


@dataclass
class InvoiceExtract:
    vendor: ExtractedField
    date: ExtractedField
    total: ExtractedField
    line_items: List[LineItem]


@dataclass
class ReceiptExtract:
    merchant: ExtractedField
    date: ExtractedField
    tax: ExtractedField
    total: ExtractedField
    line_items: List[LineItem]


@dataclass
class NormalizedExpense:
    id: str
    document_type: str
    vendor: str
    date: str
    subtotal: Optional[float]
    tax: Optional[float]
    total: float
    line_items: List[Dict[str, Any]]
    average_confidence: float
    raw_extraction: Optional[Dict[str, Any]] = None


@dataclass
class ValidationResult:
    valid: bool
    issues: List[str]
    avg_confidence: float
    min_confidence: float
