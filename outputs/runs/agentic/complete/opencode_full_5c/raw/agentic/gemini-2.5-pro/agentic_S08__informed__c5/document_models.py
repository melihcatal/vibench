from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class Invoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[LineItem] = []


class ReceiptItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    total_price: Optional[float] = None


class Receipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    items: List[ReceiptItem] = []


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total_amount: float
    line_items: List[Dict[str, Any]] = Field(default_factory=list)
    source_document_type: str
    source_document_id: str
