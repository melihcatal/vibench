import os
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"


@dataclass
class LineItem:
    description: str = ""
    quantity: float = 0.0
    unit_price: float = 0.0
    total_price: float = 0.0
    confidence: float = 0.0


@dataclass
class InvoiceFields:
    vendor_name: str = ""
    vendor_address: str = ""
    invoice_number: str = ""
    invoice_date: str = ""
    due_date: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    total: float = 0.0
    currency: str = "USD"
    line_items: list = field(default_factory=list)
    notes: str = ""
    raw_confidence: float = 0.0
    field_confidences: dict = field(default_factory=dict)


@dataclass
class ReceiptFields:
    merchant_name: str = ""
    merchant_address: str = ""
    receipt_date: str = ""
    receipt_time: str = ""
    subtotal: float = 0.0
    tax: float = 0.0
    tip: float = 0.0
    total: float = 0.0
    currency: str = "USD"
    payment_method: str = ""
    items: list = field(default_factory=list)
    raw_confidence: float = 0.0
    field_confidences: dict = field(default_factory=dict)


@dataclass
class ExpenseRecord:
    document_type: str = ""
    vendor: str = ""
    date: str = ""
    total: float = 0.0
    tax: float = 0.0
    currency: str = "USD"
    line_items: list = field(default_factory=list)
    notes: str = ""
    source_document_id: str = ""
    normalized_at: str = ""


@dataclass
class ValidationError:
    field: str
    message: str
    is_critical: bool = True


@dataclass
class ValidationResult:
    is_valid: bool = True
    errors: list = field(default_factory=list)
    confidence_warnings: list = field(default_factory=list)


@dataclass
class ExtractionRequest:
    document_path: str = ""
    document_bytes: bytes = b""
    document_type: DocumentType = DocumentType.INVOICE
    language: str = "en"


@dataclass
class ExtractionResponse:
    success: bool = False
    fields: Optional[object] = None
    error: str = ""
    provider: str = ""
    raw_response: Optional[dict] = None


def invoice_to_dict(fields: InvoiceFields) -> dict:
    return {
        "vendor_name": fields.vendor_name,
        "vendor_address": fields.vendor_address,
        "invoice_number": fields.invoice_number,
        "invoice_date": fields.invoice_date,
        "due_date": fields.due_date,
        "subtotal": fields.subtotal,
        "tax": fields.tax,
        "total": fields.total,
        "currency": fields.currency,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "confidence": item.confidence,
            }
            for item in fields.line_items
        ],
        "notes": fields.notes,
        "raw_confidence": fields.raw_confidence,
        "field_confidences": fields.field_confidences,
    }


def receipt_to_dict(fields: ReceiptFields) -> dict:
    return {
        "merchant_name": fields.merchant_name,
        "merchant_address": fields.merchant_address,
        "receipt_date": fields.receipt_date,
        "receipt_time": fields.receipt_time,
        "subtotal": fields.subtotal,
        "tax": fields.tax,
        "tip": fields.tip,
        "total": fields.total,
        "currency": fields.currency,
        "payment_method": fields.payment_method,
        "items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.total_price,
                "confidence": item.confidence,
            }
            for item in fields.items
        ],
        "raw_confidence": fields.raw_confidence,
        "field_confidences": fields.field_confidences,
    }


def normalize_to_expense_record(
    fields: object, document_type: str, source_id: str = ""
) -> ExpenseRecord:
    from datetime import datetime

    if isinstance(fields, InvoiceFields):
        return ExpenseRecord(
            document_type=document_type,
            vendor=fields.vendor_name,
            date=fields.invoice_date,
            total=fields.total,
            tax=fields.tax,
            currency=fields.currency,
            line_items=[
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in fields.line_items
            ],
            notes=fields.notes,
            source_document_id=source_id,
            normalized_at=datetime.utcnow().isoformat(),
        )
    elif isinstance(fields, ReceiptFields):
        return ExpenseRecord(
            document_type=document_type,
            vendor=fields.merchant_name,
            date=fields.receipt_date,
            total=fields.total,
            tax=fields.tax,
            currency=fields.currency,
            line_items=[
                {
                    "description": item.description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "total_price": item.total_price,
                }
                for item in fields.items
            ],
            source_document_id=source_id,
            normalized_at=datetime.utcnow().isoformat(),
        )
    return ExpenseRecord(
        document_type=document_type,
        source_document_id=source_id,
        normalized_at=datetime.utcnow().isoformat(),
    )


def expense_record_to_dict(record: ExpenseRecord) -> dict:
    return {
        "document_type": record.document_type,
        "vendor": record.vendor,
        "date": record.date,
        "total": record.total,
        "tax": record.tax,
        "currency": record.currency,
        "line_items": record.line_items,
        "notes": record.notes,
        "source_document_id": record.source_document_id,
        "normalized_at": record.normalized_at,
    }
