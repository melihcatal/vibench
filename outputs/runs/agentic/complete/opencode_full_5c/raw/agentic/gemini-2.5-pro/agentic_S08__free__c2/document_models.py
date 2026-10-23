from pydantic import BaseModel, Field
from typing import List, Optional


class InvoiceLineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    amount: float


class Invoice(BaseModel):
    vendor_name: str
    invoice_date: str
    total_amount: float
    line_items: List[InvoiceLineItem]
    confidence: float


class ReceiptItem(BaseModel):
    description: str
    quantity: float
    price: float
    total: float


class Receipt(BaseModel):
    merchant_name: str
    transaction_date: str
    tax_amount: Optional[float] = None
    total_amount: float
    items: List[ReceiptItem]
    confidence: float


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    currency: str = "USD"
    items: List[dict]
    source_document_type: str
    source_document_confidence: float
