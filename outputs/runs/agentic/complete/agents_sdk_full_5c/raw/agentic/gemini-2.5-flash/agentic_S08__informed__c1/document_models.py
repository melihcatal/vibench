import json
from typing import List, Dict, Any, Optional

class LineItem:
    def __init__(self, description: Optional[str] = None, quantity: Optional[float] = None, unit_price: Optional[float] = None, total: Optional[float] = None):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.total = total

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

class InvoiceFields:
    def __init__(self, vendor_name: Optional[str] = None, invoice_date: Optional[str] = None, total_amount: Optional[float] = None, currency: Optional[str] = None, line_items: Optional[List[LineItem]] = None):
        self.vendor_name = vendor_name
        self.invoice_date = invoice_date
        self.total_amount = total_amount
        self.currency = currency
        self.line_items = line_items if line_items is not None else []

    def to_dict(self):
        return {
            "vendor_name": self.vendor_name,
            "invoice_date": self.invoice_date,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "line_items": [item.to_dict() for item in self.line_items]
        }

class ReceiptFields:
    def __init__(self, merchant_name: Optional[str] = None, transaction_date: Optional[str] = None, total_amount: Optional[float] = None, tax_amount: Optional[float] = None, currency: Optional[str] = None, line_items: Optional[List[LineItem]] = None):
        self.merchant_name = merchant_name
        self.transaction_date = transaction_date
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.currency = currency
        self.line_items = line_items if line_items is not None else []

    def to_dict(self):
        return {
            "merchant_name": self.merchant_name,
            "transaction_date": self.transaction_date,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "line_items": [item.to_dict() for item in self.line_items]
        }

class NormalizedExpense:
    def __init__(self, document_type: str, vendor_name: Optional[str] = None, date: Optional[str] = None, total: Optional[float] = None, currency: Optional[str] = None, tax: Optional[float] = None, line_items: Optional[List[LineItem]] = None, raw_data: Optional[Dict[str, Any]] = None):
        self.document_type = document_type
        self.vendor_name = vendor_name
        self.date = date
        self.total = total
        self.currency = currency
        self.tax = tax
        self.line_items = line_items if line_items is not None else []
        self.raw_data = raw_data

    def to_dict(self):
        return {
            "document_type": self.document_type,
            "vendor_name": self.vendor_name,
            "date": self.date,
            "total": self.total,
            "currency": self.currency,
            "tax": self.tax,
            "line_items": [item.to_dict() for item in self.line_items],
            "raw_data": self.raw_data
        }

class ExtractionResult:
    def __init__(self, success: bool, data: Optional[Dict[str, Any]] = None, error: Optional[str] = None, confidence: Optional[float] = None):
        self.success = success
        self.data = data
        self.error = error
        self.confidence = confidence

    def to_dict(self):
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "confidence": self.confidence
        }
