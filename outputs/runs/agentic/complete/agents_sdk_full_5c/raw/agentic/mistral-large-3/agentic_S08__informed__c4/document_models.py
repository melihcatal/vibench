from pydantic import BaseModel
from typing import List, Optional


class LineItem(BaseModel):
    description: str
    amount: str


class InvoiceExtractionResponse(BaseModel):
    vendor: str
    date: str
    total: str
    line_items: List[LineItem]


class ReceiptItem(BaseModel):
    name: str
    price: str


class ReceiptExtractionResponse(BaseModel):
    merchant: str
    tax: str
    total: str
    items: List[ReceiptItem]


class NormalizedExpenseItem(BaseModel):
    description: str
    amount: float


class NormalizedExpense(BaseModel):
    vendor_merchant: str
    transaction_date: str
    total_amount: float
    tax_amount: float
    items: List[NormalizedExpenseItem]
    source_type: str