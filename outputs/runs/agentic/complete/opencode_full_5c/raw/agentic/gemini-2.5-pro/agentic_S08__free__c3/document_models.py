from typing import List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: float


class Invoice(BaseModel):
    vendor_name: Optional[str] = Field(None, confidence=0.0)
    invoice_date: Optional[str] = Field(None, confidence=0.0)
    total_amount: Optional[float] = Field(None, confidence=0.0)
    line_items: List[LineItem] = []


class ReceiptItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    price: Optional[float] = None
    total: float


class Receipt(BaseModel):
    merchant_name: Optional[str] = Field(None, confidence=0.0)
    total: Optional[float] = Field(None, confidence=0.0)
    tax: Optional[float] = Field(None, confidence=0.0)
    items: List[ReceiptItem] = []


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    line_items: List[dict]
    source_document_type: str
