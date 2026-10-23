from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class LineItem:
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


@dataclass
class ExtractedInvoice:
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_text: Optional[str] = None


@dataclass
class ExtractedReceipt:
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    items: List[LineItem] = field(default_factory=list)
    raw_text: Optional[str] = None


@dataclass
class NormalizedExpense:
    document_type: str  # "invoice" or "receipt"
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    tax_amount: Optional[float] = None
    document_id: Optional[str] = None
    raw_document_url: Optional[str] = None
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    vendor_notes: Optional[str] = (
        None  # For vendor_text_safety and invoice_note_translate
    )


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: Dict[str, float] = field(default_factory=dict)
    message: str = ""


@dataclass
class SummaryResult:
    summary: str


@dataclass
class SafetyResult:
    is_safe: bool
    scores: Dict[str, float] = field(default_factory=list)
    message: str = ""


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str] = None
    target_language: str = "en"  # Default to English
