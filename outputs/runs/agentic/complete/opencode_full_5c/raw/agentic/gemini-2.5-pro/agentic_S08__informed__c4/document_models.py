from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class InvoiceLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class Invoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[InvoiceLineItem] = []
    raw_fields: Dict[str, Any] = {}


class ReceiptLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    total_price: Optional[float] = None


class Receipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    line_items: List[ReceiptLineItem] = []
    raw_fields: Dict[str, Any] = {}


class NormalizedLineItem(BaseModel):
    description: str
    amount: float


class NormalizedExpense(BaseModel):
    vendor: str
    expense_date: str
    total: float
    category: Optional[str] = None
    line_items: List[NormalizedLineItem] = []
    source_document_type: str
    source_document_id: str


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
