from pydantic import BaseModel
from typing import List, Optional, Dict, Any


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
    price: Optional[float] = None
    total_price: Optional[float] = None


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    total: Optional[float] = None
    tax: Optional[float] = None

    items: List[ReceiptItem] = []
    raw_fields: Dict[str, Any] = {}


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    line_items: List[Dict[str, Any]] = []
    source_document_type: str
    raw_data: Dict[str, Any]


class ValidatedFields(BaseModel):
    is_valid: bool
    errors: List[str]
    confidence_scores: Dict[str, float]
