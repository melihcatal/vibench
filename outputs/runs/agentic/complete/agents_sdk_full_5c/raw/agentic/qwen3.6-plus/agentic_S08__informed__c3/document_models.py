"""Define local request, response, and normalization helpers for Structured Document Extraction.

Provides Pydantic models for invoice extraction, receipt extraction, expense normalization,
and document field validation results.
"""

from __future__ import annotations

import re
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from typing import Optional, Dict, List, Any

from pydantic import BaseModel, Field, field_validator


class ExpenseSource(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"


class LineItem(BaseModel):
    description: str = Field(default="", description="Line item description")
    quantity: float = Field(default=0.0, description="Line item quantity")
    unit_price: float = Field(default=0.0, description="Line item unit price")
    amount: float = Field(default=0.0, description="Line item total amount")


class InvoiceExtractionResult(BaseModel):
    vendor_name: str = Field(default="", description="Vendor/merchant name from invoice")
    invoice_date: str = Field(default="", description="Invoice date string")
    total_amount: float = Field(default=0.0, description="Invoice total amount")
    line_items: List[LineItem] = Field(default_factory=list, description="Extracted line items")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall extraction confidence")
    raw_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw extracted fields")


class ReceiptItem(BaseModel):
    description: str = Field(default="", description="Receipt item description")
    quantity: float = Field(default=0.0, description="Receipt item quantity")
    price: float = Field(default=0.0, description="Receipt item unit price")
    total_price: float = Field(default=0.0, description="Receipt item total price")


class ReceiptExtractionResult(BaseModel):
    merchant_name: str = Field(default="", description="Merchant name from receipt")
    tax_amount: float = Field(default=0.0, description="Total tax amount")
    total_amount: float = Field(default=0.0, description="Receipt total amount")
    items: List[ReceiptItem] = Field(default_factory=list, description="Extracted receipt items")
    confidence: float = Field(default=0.0, ge=0.0, le=1.0, description="Overall extraction confidence")
    raw_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw extracted fields")


class NormalizedLineItem(BaseModel):
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    amount: float = 0.0


class StandardExpenseSchema(BaseModel):
    vendor: str = Field(default="", description="Vendor name")
    date: str = Field(default="", description="ISO 8601 date string")
    total: float = Field(default=0.0, description="Total expense amount")
    tax: float = Field(default=0.0, description="Tax amount")
    currency: str = Field(default="USD", description="ISO 4217 currency code")
    line_items: List[Dict[str, Any]] = Field(default_factory=list, description="Normalized line items")
    source: str = Field(default="invoice", description="Document source type")
    confidence: float = Field(default=0.0, description="Extraction confidence")
    raw_fields: Dict[str, Any] = Field(default_factory=dict, description="Raw fields from extraction")


class NormalizedExpense(BaseModel):
    standard_schema: StandardExpenseSchema
    source_type: ExpenseSource
    normalized_at: str = Field(default="", description="ISO 8601 timestamp of normalization")


class FieldValidation(BaseModel):
    field_name: str
    present: bool
    value: Optional[Any] = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    valid: bool = True
    errors: List[str] = Field(default_factory=list)


class DocumentValidationResult(BaseModel):
    document_type: str = ""
    all_required_present: bool = True
    overall_confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    field_validations: List[FieldValidation] = Field(default_factory=list)
    valid: bool = True
    errors: List[str] = Field(default_factory=list)


# Currency normalization helpers

KNOWN_CURRENCY_SCALE = {
    "USD": 2,
    "EUR": 2,
    "GBP": 2,
    "JPY": 0,
    "CNY": 2,
    "INR": 2,
    "CAD": 2,
    "AUD": 2,
    "CHF": 2,
}


def normalize_currency_amount(amount: float, currency: str = "USD") -> float:
    """Round an amount to the standard scale for its currency.

    Uses Decimal for precise rounding with ROUND_HALF_UP.
    """
    scale = KNOWN_CURRENCY_SCALE.get(currency.upper(), 2)
    quantize_str = "0." + "0" * scale
    rounded = Decimal(str(amount)).quantize(Decimal(quantize_str), rounding=ROUND_HALF_UP)
    return float(rounded)


# Date parsing helpers

DATE_FORMATS = [
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%m-%d-%Y",
    "%d-%m-%Y",
    "%B %d, %Y",
    "%b %d, %Y",
    "%d %B %Y",
    "%d %b %Y",
    "%Y%m%d",
    "%d.%m.%Y",
]


def parse_date_to_iso(raw_date: str) -> str:
    """Try multiple date formats and return an ISO 8601 date string.

    Returns empty string if no format matches.
    """
    if not raw_date or not raw_date.strip():
        return ""

    cleaned = raw_date.strip()

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(cleaned, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # Try regex fallback for YYYY-MM-DD patterns embedded in text
    match = re.search(r"(\d{4})-(\d{1,2})-(\d{1,2})", cleaned)
    if match:
        y, m, d = match.groups()
        try:
            dt = datetime(int(y), int(m), int(d))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            pass

    # Try MM/DD/YYYY or DD/MM/YYYY
    match = re.search(r"(\d{1,2})/(\d{1,2})/(\d{4})", cleaned)
    if match:
        a, b, y = match.groups()
        try:
            dt = datetime(int(y), int(a), int(b))
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            try:
                dt = datetime(int(y), int(b), int(a))
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                pass

    return cleaned
