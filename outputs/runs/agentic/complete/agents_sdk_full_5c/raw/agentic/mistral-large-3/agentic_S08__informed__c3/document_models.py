from pydantic import BaseModel
from typing import List, Optional


class LineItem(BaseModel):
    description: str
    amount: float
    quantity: int = 1


class InvoiceResponse(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    confidence: float


class ReceiptResponse(BaseModel):
    merchant: str
    tax: float
    total: float
    items: List[LineItem]
    confidence: float


class NormalizedExpense(BaseModel):
    expense_type: str
    vendor_or_merchant: str
    date: str
    total_amount: float
    tax_amount: float
    line_items: List[LineItem]
    confidence_score: float


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]