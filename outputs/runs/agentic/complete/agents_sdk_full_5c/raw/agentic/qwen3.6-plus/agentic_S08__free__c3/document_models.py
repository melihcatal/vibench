"""Define local request, response, and normalization helpers for Structured Document Extraction."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LineItem:
    """Represents a single line item from an invoice or receipt."""
    description: str = ""
    quantity: str = ""
    unit_price: str = ""
    total_price: str = ""

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
        }


@dataclass
class ReceiptItem:
    """Represents a single item from a receipt."""
    description: str = ""
    quantity: str = ""
    price: str = ""

    def to_dict(self) -> dict:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "price": self.price,
        }


@dataclass
class InvoiceExtractionRequest:
    """Request to extract fields from an invoice document."""
    document_path: str = ""
    document_bytes: Optional[bytes] = None
    mime_type: str = "application/pdf"

    def to_dict(self) -> dict:
        return {
            "document_path": self.document_path,
            "mime_type": self.mime_type,
        }


@dataclass
class InvoiceExtractionResponse:
    """Response containing extracted invoice fields."""
    vendor: str = ""
    invoice_date: str = ""
    total_amount: str = ""
    invoice_id: str = ""
    line_items: list[LineItem] = field(default_factory=list)
    confidence: float = 0.0
    provider: str = ""

    def to_dict(self) -> dict:
        return {
            "vendor": self.vendor,
            "invoice_date": self.invoice_date,
            "total_amount": self.total_amount,
            "invoice_id": self.invoice_id,
            "line_items": [item.to_dict() for item in self.line_items],
            "confidence": self.confidence,
            "provider": self.provider,
        }


@dataclass
class ReceiptExtractionRequest:
    """Request to extract fields from a receipt document."""
    document_path: str = ""
    document_bytes: Optional[bytes] = None
    mime_type: str = "application/pdf"

    def to_dict(self) -> dict:
        return {
            "document_path": self.document_path,
            "mime_type": self.mime_type,
        }


@dataclass
class ReceiptExtractionResponse:
    """Response containing extracted receipt fields."""
    merchant: str = ""
    tax_amount: str = ""
    total_amount: str = ""
    subtotal: str = ""
    receipt_date: str = ""
    items: list[ReceiptItem] = field(default_factory=list)
    confidence: float = 0.0
    provider: str = ""

    def to_dict(self) -> dict:
        return {
            "merchant": self.merchant,
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount,
            "subtotal": self.subtotal,
            "receipt_date": self.receipt_date,
            "items": [item.to_dict() for item in self.items],
            "confidence": self.confidence,
            "provider": self.provider,
        }


@dataclass
class ExpenseNormalizationRequest:
    """Request to normalize extracted expense data."""
    source_type: str = ""  # invoice, receipt, purchase_order
    source_data: dict = field(default_factory=dict)

    @classmethod
    def from_invoice(cls, invoice_response: InvoiceExtractionResponse) -> "ExpenseNormalizationRequest":
        return cls(
            source_type="invoice",
            source_data=invoice_response.to_dict(),
        )

    @classmethod
    def from_receipt(cls, receipt_response: ReceiptExtractionResponse) -> "ExpenseNormalizationRequest":
        return cls(
            source_type="receipt",
            source_data=receipt_response.to_dict(),
        )

    def to_dict(self) -> dict:
        return {
            "source_type": self.source_type,
            "source_data": self.source_data,
        }


@dataclass
class NormalizedExpenseRecord:
    """Normalized expense record in standard JSON schema."""
    expense_type: str = ""
    vendor_name: str = ""
    document_date: Optional[str] = None
    currency: str = "USD"
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: list[dict] = field(default_factory=list)
    document_id: Optional[str] = None
    confidence: float = 0.0
    source_provider: str = ""

    def to_dict(self) -> dict:
        return {
            "expense_type": self.expense_type,
            "vendor_name": self.vendor_name,
            "document_date": self.document_date,
            "currency": self.currency,
            "subtotal": self.subtotal,
            "tax_amount": self.tax_amount,
            "total_amount": self.total_amount,
            "line_items": self.line_items,
            "document_id": self.document_id,
            "confidence": self.confidence,
            "source_provider": self.source_provider,
        }


@dataclass
class ValidationRequest:
    """Request to validate extracted document fields."""
    data: dict = field(default_factory=dict)
    required_fields: list[str] = field(default_factory=lambda: ["vendor", "date", "total"])
    min_confidence: float = 0.85

    def to_dict(self) -> dict:
        return {
            "data": self.data,
            "required_fields": self.required_fields,
            "min_confidence": self.min_confidence,
        }


@dataclass
class FieldValidation:
    """Validation result for a single field."""
    field_name: str = ""
    is_present: bool = False
    confidence_score: Optional[float] = None
    meets_threshold: bool = False
    passed: bool = False
    value: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "field_name": self.field_name,
            "is_present": self.is_present,
            "confidence_score": self.confidence_score,
            "meets_threshold": self.meets_threshold,
            "passed": self.passed,
            "value": self.value,
        }


@dataclass
class ValidationResult:
    """Overall validation result for document extraction."""
    is_valid: bool = False
    field_validations: list[FieldValidation] = field(default_factory=list)
    flagged_fields: list[str] = field(default_factory=list)
    requires_human_review: bool = False
    provider: str = ""
    min_confidence_threshold: float = 0.85
    total_amount_valid: bool = False
    date_valid: bool = False

    def to_dict(self) -> dict:
        return {
            "is_valid": self.is_valid,
            "field_validations": [fv.to_dict() for fv in self.field_validations],
            "flagged_fields": self.flagged_fields,
            "requires_human_review": self.requires_human_review,
            "provider": self.provider,
            "min_confidence_threshold": self.min_confidence_threshold,
            "total_amount_valid": self.total_amount_valid,
            "date_valid": self.date_valid,
        }


def parse_currency_amount(amount_str: str) -> Optional[float]:
    """Parse a currency string into a float value."""
    if not amount_str:
        return None
    try:
        cleaned = amount_str.replace("$", "").replace(",", "").replace(" ", "").strip()
        return float(cleaned)
    except (ValueError, TypeError):
        return None


def parse_date_to_iso(date_str: str) -> Optional[str]:
    """Attempt to parse various date formats into ISO 8601."""
    if not date_str:
        return None

    from datetime import datetime
    formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%B %d, %Y",
        "%b %d, %Y",
        "%Y%m%d",
        "%m-%d-%Y",
        "%d-%m-%Y",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str.strip(), fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return date_str
