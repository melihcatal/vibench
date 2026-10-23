import json
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class InvoiceFields(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_total: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)


class ReceiptFields(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_extraction: Dict[str, Any]
