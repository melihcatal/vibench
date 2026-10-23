from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class LineItem:
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    amount: float = 0.0
    confidence: float = 0.0


@dataclass
class ReceiptItem:
    name: str = ""
    quantity: float = 0.0
    total_price: float = 0.0
    confidence: float = 0.0


@dataclass
class InvoiceExtractionResult:
    vendor_name: str = ""
    vendor_address: str = ""
    invoice_id: str = ""
    invoice_date: str = ""
    due_date: str = ""
    subtotal: float = 0.0
    total_tax: float = 0.0
    total_amount: float = 0.0
    currency: str = ""
    line_items: List[LineItem] = field(default_factory=list)
    notes: str = ""
    raw_confidence: float = 0.0
    field_confidences: Dict[str, float] = field(default_factory=dict)


@dataclass
class ReceiptExtractionResult:
    merchant_name: str = ""
    merchant_address: str = ""
    transaction_date: str = ""
    transaction_time: str = ""
    subtotal: float = 0.0
    total_tax: float = 0.0
    total_amount: float = 0.0
    currency: str = ""
    items: List[ReceiptItem] = field(default_factory=list)
    raw_confidence: float = 0.0
    field_confidences: Dict[str, float] = field(default_factory=dict)


@dataclass
class NormalizedExpenseRecord:
    document_type: str = ""
    document_id: str = ""
    vendor_or_merchant: str = ""
    date: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    currency: str = "USD"
    line_items: List[Dict[str, Any]] = field(default_factory=list)
    raw_confidence: float = 0.0
    extracted_at: str = ""
    source_model: str = ""
    validation_status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


REQUIRED_INVOICE_FIELDS = ["vendor_name", "invoice_date", "total_amount"]
REQUIRED_RECEIPT_FIELDS = ["merchant_name", "transaction_date", "total_amount"]
MINIMUM_CONFIDENCE_THRESHOLD = 0.7


def normalize_invoice_to_expense(
    invoice_result: InvoiceExtractionResult,
    source_model: str = "azure-di-prebuilt-invoice",
) -> NormalizedExpenseRecord:
    items = []
    for li in invoice_result.line_items:
        items.append(
            {
                "description": li.description,
                "quantity": li.quantity,
                "unit_price": li.unit_price,
                "amount": li.amount,
            }
        )
    return NormalizedExpenseRecord(
        document_type="invoice",
        document_id=invoice_result.invoice_id,
        vendor_or_merchant=invoice_result.vendor_name,
        date=invoice_result.invoice_date,
        subtotal=invoice_result.subtotal,
        tax=invoice_result.total_tax,
        total=invoice_result.total_amount,
        currency=invoice_result.currency or "USD",
        line_items=items,
        raw_confidence=invoice_result.raw_confidence,
        extracted_at=datetime.utcnow().isoformat(),
        source_model=source_model,
        metadata={"notes": invoice_result.notes, "due_date": invoice_result.due_date},
    )


def normalize_receipt_to_expense(
    receipt_result: ReceiptExtractionResult,
    source_model: str = "azure-di-prebuilt-receipt",
) -> NormalizedExpenseRecord:
    items = []
    for item in receipt_result.items:
        items.append(
            {
                "description": item.name,
                "quantity": item.quantity,
                "amount": item.total_price,
            }
        )
    return NormalizedExpenseRecord(
        document_type="receipt",
        document_id=f"rcpt_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
        vendor_or_merchant=receipt_result.merchant_name,
        date=receipt_result.transaction_date,
        subtotal=receipt_result.subtotal,
        tax=receipt_result.total_tax,
        total=receipt_result.total_amount,
        currency=receipt_result.currency or "USD",
        line_items=items,
        raw_confidence=receipt_result.raw_confidence,
        extracted_at=datetime.utcnow().isoformat(),
        source_model=source_model,
    )


def validate_invoice_fields(
    result: InvoiceExtractionResult, required_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    fields_to_check = required_fields or REQUIRED_INVOICE_FIELDS
    missing = []
    low_confidence = []
    for f in fields_to_check:
        value = getattr(result, f, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(f)
        conf = result.field_confidences.get(f, 0.0)
        if conf < MINIMUM_CONFIDENCE_THRESHOLD:
            low_confidence.append({"field": f, "confidence": conf})
    return {
        "valid": len(missing) == 0 and len(low_confidence) == 0,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "overall_confidence": result.raw_confidence,
    }


def validate_receipt_fields(
    result: ReceiptExtractionResult, required_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    fields_to_check = required_fields or REQUIRED_RECEIPT_FIELDS
    missing = []
    low_confidence = []
    for f in fields_to_check:
        value = getattr(result, f, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(f)
        conf = result.field_confidences.get(f, 0.0)
        if conf < MINIMUM_CONFIDENCE_THRESHOLD:
            low_confidence.append({"field": f, "confidence": conf})
    return {
        "valid": len(missing) == 0 and len(low_confidence) == 0,
        "missing_fields": missing,
        "low_confidence_fields": low_confidence,
        "overall_confidence": result.raw_confidence,
    }


def validate_expense_record(record: NormalizedExpenseRecord) -> Dict[str, Any]:
    required = ["document_type", "document_id", "vendor_or_merchant", "date", "total"]
    missing = []
    for f in required:
        value = getattr(record, f, None)
        if value is None or (isinstance(value, str) and not value.strip()):
            missing.append(f)
    return {
        "valid": len(missing) == 0,
        "missing_fields": missing,
        "validation_status": "valid" if len(missing) == 0 else "invalid",
    }
