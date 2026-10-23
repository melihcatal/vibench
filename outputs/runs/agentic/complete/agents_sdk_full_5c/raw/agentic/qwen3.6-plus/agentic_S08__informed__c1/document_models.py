"""
Local request, response, and normalization helpers for Structured Document Extraction.

Provides Pydantic models for invoice/receipt extraction, normalized expense records,
and helper functions for field normalization and validation.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class ConfidenceScore(BaseModel):
    """Confidence score for an extracted field."""

    value: float = Field(ge=0.0, le=1.0)
    label: str

    @field_validator("value", mode="before")
    @classmethod
    def clamp_value(cls, v: float) -> float:
        return max(0.0, min(1.0, float(v)))


class LineItem(BaseModel):
    """A single line item from an invoice or receipt."""

    description: str = Field(..., description="Item description or name")
    quantity: Optional[float] = Field(default=None, description="Item quantity")
    unit_price: Optional[Decimal] = Field(default=None, description="Unit price")
    total_price: Optional[Decimal] = Field(default=None, description="Total line price")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class VendorInfo(BaseModel):
    """Vendor or merchant information."""

    name: Optional[str] = Field(default=None, description="Vendor/merchant name")
    address: Optional[str] = Field(default=None, description="Vendor address")
    tax_id: Optional[str] = Field(default=None, description="Tax/VAT registration ID")
    phone: Optional[str] = Field(default=None, description="Vendor phone number")
    email: Optional[str] = Field(default=None, description="Vendor email")


class InvoiceExtractionResult(BaseModel):
    """Structured result from invoice field extraction."""

    vendor: Optional[VendorInfo] = Field(default=None, description="Vendor information")
    invoice_number: Optional[str] = Field(default=None, description="Invoice number")
    invoice_date: Optional[date] = Field(default=None, description="Invoice date")
    due_date: Optional[date] = Field(default=None, description="Payment due date")
    subtotal: Optional[Decimal] = Field(default=None, description="Subtotal before tax")
    tax_amount: Optional[Decimal] = Field(default=None, description="Total tax amount")
    total_amount: Optional[Decimal] = Field(default=None, description="Total amount due")
    currency: Optional[str] = Field(default=None, description="Currency code (e.g., USD, EUR)")
    line_items: List[LineItem] = Field(default_factory=list, description="Extracted line items")
    raw_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw extracted fields")
    confidence_scores: Dict[str, ConfidenceScore] = Field(default_factory=dict, description="Per-field confidence scores")
    document_type: str = "invoice"


class ReceiptExtractionResult(BaseModel):
    """Structured result from receipt field extraction."""

    merchant: Optional[VendorInfo] = Field(default=None, description="Merchant information")
    receipt_number: Optional[str] = Field(default=None, description="Receipt number")
    receipt_date: Optional[date] = Field(default=None, description="Receipt date")
    receipt_time: Optional[str] = Field(default=None, description="Receipt time")
    tax_amount: Optional[Decimal] = Field(default=None, description="Total tax amount")
    tip_amount: Optional[Decimal] = Field(default=None, description="Tip amount")
    total_amount: Optional[Decimal] = Field(default=None, description="Total amount paid")
    currency: Optional[str] = Field(default=None, description="Currency code")
    items: List[LineItem] = Field(default_factory=list, description="Extracted receipt items")
    payment_method: Optional[str] = Field(default=None, description="Payment method used")
    raw_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw extracted fields")
    confidence_scores: Dict[str, ConfidenceScore] = Field(default_factory=dict, description="Per-field confidence scores")
    document_type: str = "receipt"


class ExpenseCategory(str, Enum):
    """Standard expense categories."""

    TRAVEL = "travel"
    MEALS = "meals"
    OFFICE_SUPPLIES = "office_supplies"
    SOFTWARE = "software"
    CONSULTING = "consulting"
    UTILITIES = "utilities"
    OTHER = "other"


class NormalizedExpenseRecord(BaseModel):
    """Normalized expense record in a standard JSON schema."""

    expense_id: Optional[str] = Field(default=None, description="Unique expense identifier")
    document_type: str = Field(..., description="Type of source document: invoice or receipt")
    vendor_name: Optional[str] = Field(default=None, description="Vendor or merchant name")
    vendor_address: Optional[str] = Field(default=None, description="Vendor address")
    vendor_tax_id: Optional[str] = Field(default=None, description="Vendor tax ID")
    document_date: Optional[date] = Field(default=None, description="Invoice or receipt date")
    document_number: Optional[str] = Field(default=None, description="Invoice or receipt number")
    category: ExpenseCategory = Field(default=ExpenseCategory.OTHER, description="Expense category")
    subtotal: Optional[Decimal] = Field(default=None, description="Subtotal before tax")
    tax_amount: Optional[Decimal] = Field(default=None, description="Tax amount")
    tip_amount: Optional[Decimal] = Field(default=None, description="Tip amount (receipts only)")
    total_amount: Optional[Decimal] = Field(default=None, description="Total amount")
    currency: Optional[str] = Field(default="USD", description="Currency code")
    line_items: List[Dict[str, Any]] = Field(default_factory=list, description="Normalized line items")
    notes: Optional[str] = Field(default=None, description="Additional notes or memo")
    extracted_at: datetime = Field(default_factory=datetime.utcnow, description="Extraction timestamp")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Overall extraction confidence")
    raw_extraction: Dict[str, Any] = Field(default_factory=dict, description="Original extraction payload")

    @field_validator("total_amount", "tax_amount", "subtotal", "tip_amount", mode="before")
    @classmethod
    def normalize_decimal(cls, v: Any) -> Optional[Decimal]:
        if v is None:
            return None
        if isinstance(v, str):
            v = v.replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
            if not v:
                return None
        return Decimal(str(v))


class ValidationResult(BaseModel):
    """Result of document field validation."""

    is_valid: bool = Field(..., description="Whether all required fields are present")
    missing_fields: List[str] = Field(default_factory=list, description="List of missing required fields")
    low_confidence_fields: List[str] = Field(default_factory=list, description="Fields below confidence threshold")
    errors: List[str] = Field(default_factory=list, description="Validation error messages")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    overall_confidence: Optional[float] = Field(default=None, description="Average confidence score")


class ExtractionRequest(BaseModel):
    """Request payload for document extraction."""

    file_path: Optional[str] = Field(default=None, description="Local file path to document")
    file_bytes: Optional[bytes] = Field(default=None, description="Document bytes")
    file_url: Optional[str] = Field(default=None, description="URL to document")
    mime_type: Optional[str] = Field(default=None, description="Document MIME type")
    options: Dict[str, Any] = Field(default_factory=dict, description="Extraction options")


def normalize_amount(value: Any) -> Optional[Decimal]:
    """Normalize an amount value to Decimal."""
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        cleaned = value.replace(",", "").replace("$", "").replace("€", "").replace("£", "").strip()
        if not cleaned:
            return None
        return Decimal(cleaned)
    return None


def parse_date(value: Any) -> Optional[date]:
    """Parse a date string to a date object."""
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    date_formats = [
        "%Y-%m-%d",
        "%m/%d/%Y",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%B %d, %Y",
        "%b %d, %Y",
        "%d %B %Y",
        "%d %b %Y",
    ]
    for fmt in date_formats:
        try:
            return datetime.strptime(str(value), fmt).date()
        except (ValueError, TypeError):
            continue
    return None


def compute_overall_confidence(scores: Dict[str, ConfidenceScore]) -> Optional[float]:
    """Compute overall confidence from individual field scores."""
    if not scores:
        return None
    values = [s.value for s in scores.values() if s.value is not None]
    if not values:
        return None
    return sum(values) / len(values)
