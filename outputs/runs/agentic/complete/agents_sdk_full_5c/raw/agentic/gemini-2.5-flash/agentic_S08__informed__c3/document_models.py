"""
document_models.py

Defines local request, response, and normalization helpers for Structured Document Extraction.
"""

from typing import List, Dict, Any, Optional
from datetime import date

class LineItem:
    def __init__(self, description: Optional[str] = None, quantity: Optional[float] = None,
                 unit_price: Optional[float] = None, amount: Optional[float] = None):
        self.description = description
        self.quantity = quantity
        self.unit_price = unit_price
        self.amount = amount

    def to_dict(self):
        return {
            "description": self.description,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount
        }

class Expense:
    def __init__(self,
                 document_type: str,
                 vendor_name: Optional[str] = None,
                 transaction_date: Optional[date] = None,
                 total_amount: Optional[float] = None,
                 currency: Optional[str] = None,
                 tax_amount: Optional[float] = None,
                 line_items: Optional[List[LineItem]] = None,
                 original_data: Optional[Dict[str, Any]] = None,
                 notes: Optional[str] = None):
        self.document_type = document_type
        self.vendor_name = vendor_name
        self.transaction_date = transaction_date
        self.total_amount = total_amount
        self.currency = currency
        self.tax_amount = tax_amount
        self.line_items = line_items if line_items is not None else []
        self.original_data = original_data if original_data is not None else {}
        self.notes = notes

    def to_dict(self):
        return {
            "document_type": self.document_type,
            "vendor_name": self.vendor_name,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "tax_amount": self.tax_amount,
            "line_items": [item.to_dict() for item in self.line_items],
            "original_data": self.original_data,
            "notes": self.notes
        }
