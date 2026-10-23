from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class LineItem:
    description: str
    quantity: float
    unit_price: float
    amount: float


@dataclass
class InvoiceExtraction:
    vendor_name: str
    invoice_date: str
    invoice_number: str
    total_amount: float
    tax_amount: float
    currency: str
    line_items: List[LineItem] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self):
        return {
            "vendor_name": self.vendor_name,
            "invoice_date": self.invoice_date,
            "invoice_number": self.invoice_number,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "line_items": [asdict(item) for item in self.line_items],
            "confidence_scores": self.confidence_scores,
        }


@dataclass
class ReceiptExtraction:
    merchant_name: str
    transaction_date: str
    total_amount: float
    tax_amount: float
    currency: str
    items: List[Dict[str, Any]] = field(default_factory=list)
    confidence_scores: Dict[str, float] = field(default_factory=dict)

    def to_dict(self):
        return {
            "merchant_name": self.merchant_name,
            "transaction_date": self.transaction_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "items": self.items,
            "confidence_scores": self.confidence_scores,
        }


@dataclass
class NormalizedExpense:
    document_type: str
    vendor: str
    date: str
    total: float
    tax: float
    currency: str
    line_items: List[Dict[str, Any]]
    source_document_id: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        result = asdict(self)
        return result


@dataclass
class FieldValidation:
    field_name: str
    present: bool
    confidence: float
    valid: bool
    message: str = ""


@dataclass
class ValidationResult:
    is_valid: bool
    field_results: List[FieldValidation]
    warnings: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            "is_valid": self.is_valid,
            "field_results": [asdict(f) for f in self.field_results],
            "warnings": self.warnings,
        }
