from typing import List, Dict, Any, Optional
from datetime import datetime

# Define Pydantic-like models for structured document data
# These models help in normalizing and validating the extracted fields.

class ExtractedLineItem:
    description: Optional[str] = None
    amount: Optional[float] = None
    quantity: Optional[int] = None

    def __init__(self, description: str = None, amount: float = None, quantity: int = None):
        self.description = description
        self.amount = amount
        self.quantity = quantity

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "quantity": self.quantity,
        }

class NormalizedExpenseSchema:
    document_type: str  # e.g., "invoice" or "receipt"
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_date: Optional[datetime] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[ExtractedLineItem]
    original_source_data: Dict[str, Any]

    def __init__(
        self, 
        document_type: str,
        vendor_name: str = None,
        merchant_name: str = None,
        transaction_date: datetime = None,
        total_amount: float = None,
        tax_amount: float = None,
        currency: str = None,
        line_items: List[ExtractedLineItem] = None,
        original_source_data: Dict[str, Any] = None
    ):
        self.document_type = document_type
        self.vendor_name = vendor_name
        self.merchant_name = merchant_name
        self.transaction_date = transaction_date
        self.total_amount = total_amount
        self.tax_amount = tax_amount
        self.currency = currency
        self.line_items = line_items if line_items is not None else []
        self.original_source_data = original_source_data if original_source_data is not None else {}

    def to_dict(self):
        return {
            "document_type": self.document_type,
            "vendor_name": self.vendor_name,
            "merchant_name": self.merchant_name,
            "transaction_date": self.transaction_date.isoformat() if self.transaction_date else None,
            "total_amount": self.total_amount,
            "tax_amount": self.tax_amount,
            "currency": self.currency,
            "line_items": [item.to_dict() for item in self.line_items],
            "original_source_data": self.original_source_data,
        }
