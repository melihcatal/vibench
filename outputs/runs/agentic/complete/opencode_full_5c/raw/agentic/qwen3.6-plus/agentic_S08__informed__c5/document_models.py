from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import date, datetime


@dataclass
class FieldWithConfidence:
    value: Any
    confidence: float = 0.0


@dataclass
class LineItem:
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    amount: float = 0.0
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "confidence": self.confidence,
        }


@dataclass
class InvoiceExtractionResult:
    vendor_name: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    invoice_date: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    invoice_total: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence(0.0)
    )
    invoice_sub_total: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence(0.0)
    )
    invoice_tax: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence(0.0)
    )
    invoice_id: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    billing_address: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    line_items: List[LineItem] = field(default_factory=list)
    raw_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor_name": asdict(self.vendor_name),
            "invoice_date": asdict(self.invoice_date),
            "invoice_total": asdict(self.invoice_total),
            "invoice_sub_total": asdict(self.invoice_sub_total),
            "invoice_tax": asdict(self.invoice_tax),
            "invoice_id": asdict(self.invoice_id),
            "billing_address": asdict(self.billing_address),
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_fields": self.raw_fields,
        }


@dataclass
class ReceiptExtractionResult:
    merchant_name: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    transaction_date: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    transaction_total: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence(0.0)
    )
    tax: FieldWithConfidence = field(default_factory=lambda: FieldWithConfidence(0.0))
    subtotal: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence(0.0)
    )
    receipt_id: FieldWithConfidence = field(
        default_factory=lambda: FieldWithConfidence("")
    )
    items: List[LineItem] = field(default_factory=list)
    raw_fields: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "merchant_name": asdict(self.merchant_name),
            "transaction_date": asdict(self.transaction_date),
            "transaction_total": asdict(self.transaction_total),
            "tax": asdict(self.tax),
            "subtotal": asdict(self.subtotal),
            "receipt_id": asdict(self.receipt_id),
            "items": [item.to_dict() for item in self.items],
            "raw_fields": self.raw_fields,
        }


@dataclass
class NormalizedExpenseRecord:
    source_type: str = ""
    vendor_or_merchant: str = ""
    document_date: str = ""
    total_amount: float = 0.0
    tax_amount: float = 0.0
    subtotal_amount: float = 0.0
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    document_id: str = ""
    normalized_at: str = ""
    confidence_overall: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_type": self.source_type,
            "vendor_or_merchant": self.vendor_or_merchant,
            "document_date": self.document_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "subtotal_amount": self.subtotal_amount,
            "currency": self.currency,
            "line_items": self.line_items,
            "document_id": self.document_id,
            "normalized_at": self.normalized_at,
            "confidence_overall": self.confidence_overall,
        }


def normalize_invoice_to_expense(
    invoice_result: InvoiceExtractionResult,
) -> NormalizedExpenseRecord:
    import datetime

    confidences = [
        invoice_result.vendor_name.confidence,
        invoice_result.invoice_date.confidence,
        invoice_result.invoice_total.confidence,
    ]
    avg_confidence = sum(c for c in confidences if c > 0) / max(
        len([c for c in confidences if c > 0]), 1
    )
    doc_date = invoice_result.invoice_date.value
    if isinstance(doc_date, (date, datetime)):
        doc_date = doc_date.isoformat()
    return NormalizedExpenseRecord(
        source_type="invoice",
        vendor_or_merchant=invoice_result.vendor_name.value or "",
        document_date=str(doc_date) if doc_date else "",
        total_amount=float(invoice_result.invoice_total.value or 0.0),
        tax_amount=float(invoice_result.invoice_tax.value or 0.0),
        subtotal_amount=float(invoice_result.invoice_sub_total.value or 0.0),
        line_items=[item.to_dict() for item in invoice_result.line_items],
        document_id=invoice_result.invoice_id.value or "",
        normalized_at=datetime.datetime.utcnow().isoformat(),
        confidence_overall=round(avg_confidence, 4),
    )


def normalize_receipt_to_expense(
    receipt_result: ReceiptExtractionResult,
) -> NormalizedExpenseRecord:
    import datetime

    confidences = [
        receipt_result.merchant_name.confidence,
        receipt_result.transaction_date.confidence,
        receipt_result.transaction_total.confidence,
    ]
    avg_confidence = sum(c for c in confidences if c > 0) / max(
        len([c for c in confidences if c > 0]), 1
    )
    doc_date = receipt_result.transaction_date.value
    if isinstance(doc_date, (date, datetime)):
        doc_date = doc_date.isoformat()
    return NormalizedExpenseRecord(
        source_type="receipt",
        vendor_or_merchant=receipt_result.merchant_name.value or "",
        document_date=str(doc_date) if doc_date else "",
        total_amount=float(receipt_result.transaction_total.value or 0.0),
        tax_amount=float(receipt_result.tax.value or 0.0),
        subtotal_amount=float(receipt_result.subtotal.value or 0.0),
        line_items=[item.to_dict() for item in receipt_result.items],
        document_id=receipt_result.receipt_id.value or "",
        normalized_at=datetime.datetime.utcnow().isoformat(),
        confidence_overall=round(avg_confidence, 4),
    )
