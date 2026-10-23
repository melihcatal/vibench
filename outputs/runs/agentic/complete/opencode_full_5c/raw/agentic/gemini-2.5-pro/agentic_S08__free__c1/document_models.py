from pydantic import BaseModel, Field
from typing import List, Optional, Union


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: float


class Invoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_date: Optional[str] = None
    due_date: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: float
    currency: Optional[str] = None
    line_items: List[LineItem] = []


class Receipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    transaction_time: Optional[str] = None
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: float
    currency: Optional[str] = None
    line_items: List[LineItem] = []


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    currency: str
    items: List[LineItem]
    source_document_type: str
    source_document_id: Optional[str] = None
