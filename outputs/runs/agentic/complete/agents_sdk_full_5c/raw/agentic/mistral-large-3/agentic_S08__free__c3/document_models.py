from pydantic import BaseModel
from typing import List, Optional


class LineItem(BaseModel):
    description: str
    amount: float


class InvoiceExtractionResponse(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]


class ReceiptItem(BaseModel):
    description: str
    price: float


class ReceiptExtractionResponse(BaseModel):
    merchant: str
    tax: float
    total: float
    items: List[ReceiptItem]


class NormalizedExpense(BaseModel):
    vendor: str
    date: str
    amount: float
    category: str
    items: List
    tax: float


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    confidence: float