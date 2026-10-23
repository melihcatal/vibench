from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class InvoiceLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[InvoiceLineItem] = []
    raw_fields: Dict[str, Any] = {}


class ReceiptItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    total_price: Optional[float] = None


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    items: List[ReceiptItem] = []
    raw_fields: Dict[str, Any] = {}


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    currency: str = "USD"
    category: str = "Uncategorized"
    line_items: List[Dict[str, Any]] = []


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str] = Field(default_factory=list)
