"""
Define local request, response, and normalization helpers for Structured Document Extraction.
Provides Pydantic-like data classes for invoices, receipts, expenses, and validation results.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime
import json


@dataclass
class ConfidenceScore:
    """Represents a confidence score for a single extracted field."""
    field_name: str
    score: float
    confidence_level: str = field(init=False)

    def __post_init__(self):
        if self.score >= 0.9:
            self.confidence_level = "high"
        elif self.score >= 0.7:
            self.confidence_level = "medium"
        elif self.score >= 0.5:
            self.confidence_level = "low"
        else:
            self.confidence_level = "very_low"


@dataclass
class InvoiceLineItem:
    """Represents a single line item from an invoice."""
    description: str
    quantity: float
    unit_price: float
    total_price: float
    confidence: Optional[ConfidenceScore] = None


@dataclass
class InvoiceExtractionResult:
    """Complete invoice extraction result with vendor and line items."""
    vendor: str
    invoice_number: str
    invoice_date: str
    total_amount: float
    currency: str = "USD"
    line_items: List[InvoiceLineItem] = field(default_factory=list)
    confidence_scores: List[ConfidenceScore] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class ReceiptItem:
    """Represents a single item from a receipt."""
    name: str
    price: float
    quantity: Optional[float] = 1.0


@dataclass
class ReceiptExtractionResult:
    """Complete receipt extraction result."""
    merchant: str
    transaction_date: str
    tax_amount: float
    total_amount: float
    currency: str = "USD"
    items: List[ReceiptItem] = field(default_factory=list)
    confidence_scores: List[ConfidenceScore] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class NormalizedExpenseRecord:
    """Normalized expense record conforming to standard schema."""
    expense_type: str  # "invoice" or "receipt"
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str
    tax_amount: float = 0.0
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    document_id: str = ""
    source_system: str = ""
    extracted_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    validation_status: str = "pending"

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps(asdict(self), indent=2)

    @classmethod
    def from_invoice(cls, invoice: InvoiceExtractionResult, document_id: str = "", source: str = "") -> "NormalizedExpenseRecord":
        """Create normalized record from invoice extraction."""
        return cls(
            expense_type="invoice",
            vendor_name=invoice.vendor,
            transaction_date=invoice.invoice_date,
            total_amount=invoice.total_amount,
            currency=invoice.currency,
            line_items=[
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in invoice.line_items
            ],
            document_id=document_id,
            source_system=source,
        )

    @classmethod
    def from_receipt(cls, receipt: ReceiptExtractionResult, document_id: str = "", source: str = "") -> "NormalizedExpenseRecord":
        """Create normalized record from receipt extraction."""
        return cls(
            expense_type="receipt",
            vendor_name=receipt.merchant,
            transaction_date=receipt.transaction_date,
            total_amount=receipt.total_amount,
            currency=receipt.currency,
            tax_amount=receipt.tax_amount,
            line_items=[
                {
                    "description": item.name,
                    "quantity": item.quantity,
                    "unit_price": item.price,
                    "total_price": item.price * (item.quantity or 1.0),
                }
                for item in receipt.items
            ],
            document_id=document_id,
            source_system=source,
        )


@dataclass
class FieldValidationResult:
    """Result of validating required document fields."""
    document_type: str
    is_valid: bool
    required_fields_present: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    validation_timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


def build_confidence_scores(field_scores: Dict[str, float]) -> List[ConfidenceScore]:
    """Build confidence score list from field name to score mapping."""
    return [
        ConfidenceScore(field_name=name, score=score)
        for name, score in field_scores.items()
    ]
