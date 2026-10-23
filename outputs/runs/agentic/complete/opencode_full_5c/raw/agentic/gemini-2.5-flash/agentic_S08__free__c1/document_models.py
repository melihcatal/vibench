from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional


class ExtractedLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[ExtractedLineItem] = []
    notes: Optional[str] = None  # For later-step integration


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[ExtractedLineItem] = []
    items: List[str] = []  # Simpler item list for receipts for now


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[ExtractedLineItem] = []
    original_document_data: Dict[str, Any]
    notes: Optional[str] = None  # For later-step integration
