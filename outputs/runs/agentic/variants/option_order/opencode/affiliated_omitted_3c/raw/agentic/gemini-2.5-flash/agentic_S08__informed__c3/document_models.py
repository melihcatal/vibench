import datetime
from typing import Dict, List, Optional, Any


class ExtractedField:
    def __init__(self, value: Any, confidence: float):
        self.value = value
        self.confidence = confidence


class InvoiceLineItem:
    def __init__(
        self,
        description: Optional[str] = None,
        quantity: Optional[float] = None,
        unit_price: Optional[float] = None,
        amount: Optional[float] = None,
    ):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.amount = amount


class ExtractedInvoice:
    def __init__(
        self,
        vendor_name: Optional[ExtractedField] = None,
        invoice_date: Optional[ExtractedField] = None,
        total_amount: Optional[ExtractedField] = None,
        line_items: Optional[List[InvoiceLineItem]] = None,
        vendor_address: Optional[ExtractedField] = None,
        customer_name: Optional[ExtractedField] = None,
        purchase_order: Optional[ExtractedField] = None,
        due_date: Optional[ExtractedField] = None,
        currency: Optional[ExtractedField] = None,
        invoice_id: Optional[ExtractedField] = None,
        subtotal: Optional[ExtractedField] = None,
        total_tax: Optional[ExtractedField] = None,
    ):
        self.vendor_name = vendor_name
        self.invoice_date = invoice_date
        self.total_amount = total_amount
        self.line_items = line_items if line_items is not None else []
        self.vendor_address = vendor_address
        self.customer_name = customer_name
        self.purchase_order = purchase_order
        self.due_date = due_date
        self.currency = currency
        self.invoice_id = invoice_id
        self.subtotal = subtotal
        self.total_tax = total_tax


class ReceiptItem:
    def __init__(
        self,
        description: Optional[str] = None,
        quantity: Optional[float] = None,
        price: Optional[float] = None,
        total_price: Optional[float] = None,
    ):
        self.description = description
        self.quantity = quantity
        self.price = price
        self.total_price = total_price


class ExtractedReceipt:
    def __init__(
        self,
        merchant_name: Optional[ExtractedField] = None,
        transaction_date: Optional[ExtractedField] = None,
        total_amount: Optional[ExtractedField] = None,
        total_tax: Optional[ExtractedField] = None,
        items: Optional[List[ReceiptItem]] = None,
        currency: Optional[ExtractedField] = None,
        merchant_address: Optional[ExtractedField] = None,
    ):
        self.merchant_name = merchant_name
        self.transaction_date = transaction_date
        self.total_amount = total_amount
        self.total_tax = total_tax
        self.items = items if items is not None else []
        self.currency = currency
        self.merchant_address = merchant_address


class NormalizedExpense:
    def __init__(
        self,
        document_type: str,
        vendor_name: Optional[str] = None,
        transaction_date: Optional[str] = None,
        total_amount: Optional[float] = None,
        currency: Optional[str] = None,
        line_items: Optional[List[Dict[str, Any]]] = None,
        tax_amount: Optional[float] = None,
        memo_field: Optional[str] = None,
        raw_extraction: Optional[Dict[str, Any]] = None,
    ):
        self.document_type = document_type
        self.vendor_name = vendor_name
        self.transaction_date = transaction_date
        self.total_amount = total_amount
        self.currency = currency
        self.line_items = line_items if line_items is not None else []
        self.tax_amount = tax_amount
        self.memo_field = memo_field
        self.raw_extraction = raw_extraction


class ValidationResult:
    def __init__(
        self,
        field_name: str,
        is_valid: bool,
        reason: Optional[str] = None,
        confidence: Optional[float] = None,
    ):
        self.field_name = field_name
        self.is_valid = is_valid
        self.reason = reason
        self.confidence = confidence


class InvoiceSummary:
    def __init__(self, summary_text: str, key_phrases: Optional[List[str]] = None):
        self.summary_text = summary_text
        self.key_phrases = key_phrases if key_phrases is not None else []


class ModerationResult:
    def __init__(
        self,
        is_safe: bool,
        categories: Optional[Dict[str, Any]] = None,
        text: Optional[str] = None,
    ):
        self.is_safe = is_safe
        self.categories = categories
        self.text = text


class TranslationResult:
    def __init__(
        self,
        translated_text: str,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ):
        self.translated_text = translated_text
        self.source_language = source_language
        self.target_language = target_language
