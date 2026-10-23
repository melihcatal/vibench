from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class ExtractedField:
    name: str
    value: str
    confidence: float
    page: int = 1


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    total: float
    confidence: float = 1.0


@dataclass
class InvoiceExtraction:
    vendor: str = ""
    invoice_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    raw_fields: Dict[str, ExtractedField] = field(default_factory=dict)
    confidence_overall: float = 0.0


@dataclass
class ReceiptExtraction:
    merchant: str = ""
    receipt_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    currency: str = "USD"
    items: List[Dict[str, Any]] = field(default_factory=list)
    raw_fields: Dict[str, ExtractedField] = field(default_factory=dict)
    confidence_overall: float = 0.0


@dataclass
class NormalizedExpense:
    document_type: str = ""
    vendor_or_merchant: str = ""
    transaction_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    normalized_at: str = ""

    def to_json(self) -> Dict[str, Any]:
        return {
            "document_type": self.document_type,
            "vendor_or_merchant": self.vendor_or_merchant,
            "transaction_date": self.transaction_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "line_items": self.line_items,
            "metadata": self.metadata,
            "normalized_at": self.normalized_at,
        }


@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    confidence_threshold: float = 0.7
    details: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "missing_fields": self.missing_fields,
            "low_confidence_fields": self.low_confidence_fields,
            "confidence_threshold": self.confidence_threshold,
            "details": self.details,
        }


@dataclass
class InvoiceSummary:
    vendor: str = ""
    invoice_date: str = ""
    total_amount: float = 0.0
    line_item_count: int = 0
    summary_text: str = ""
    generated_at: str = ""

    def to_json(self) -> Dict[str, Any]:
        return {
            "vendor": self.vendor,
            "invoice_date": self.invoice_date,
            "total_amount": self.total_amount,
            "line_item_count": self.line_item_count,
            "summary_text": self.summary_text,
            "generated_at": self.generated_at,
        }


@dataclass
class ModerationResult:
    is_safe: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    category_scores: Dict[str, float] = field(default_factory=dict)
    flagged_reasons: List[str] = field(default_factory=list)

    def to_json(self) -> Dict[str, Any]:
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "category_scores": self.category_scores,
            "flagged_reasons": self.flagged_reasons,
        }


@dataclass
class TranslationResult:
    source_text: str = ""
    translated_text: str = ""
    source_language: str = "auto"
    target_language: str = "en"
    confidence: float = 1.0

    def to_json(self) -> Dict[str, Any]:
        return {
            "source_text": self.source_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "confidence": self.confidence,
        }


@dataclass
class StoredRecord:
    record_id: str
    document: NormalizedExpense
    stored_at: str
    status: str = "stored"

    def to_json(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "document": self.document.to_json(),
            "stored_at": self.stored_at,
            "status": self.status,
        }


def invoice_to_normalized(invoice: InvoiceExtraction) -> NormalizedExpense:
    return NormalizedExpense(
        document_type="invoice",
        vendor_or_merchant=invoice.vendor,
        transaction_date=invoice.invoice_date,
        total_amount=invoice.total_amount,
        tax_amount=invoice.tax_amount,
        currency=invoice.currency,
        line_items=[asdict(li) for li in invoice.line_items],
        metadata={
            "confidence_overall": invoice.confidence_overall,
            "raw_field_count": len(invoice.raw_fields),
        },
        normalized_at=datetime.utcnow().isoformat(),
    )


def receipt_to_normalized(receipt: ReceiptExtraction) -> NormalizedExpense:
    return NormalizedExpense(
        document_type="receipt",
        vendor_or_merchant=receipt.merchant,
        transaction_date=receipt.receipt_date,
        total_amount=receipt.total_amount,
        tax_amount=receipt.tax_amount,
        currency=receipt.currency,
        line_items=receipt.items,
        metadata={
            "confidence_overall": receipt.confidence_overall,
            "raw_field_count": len(receipt.raw_fields),
        },
        normalized_at=datetime.utcnow().isoformat(),
    )
