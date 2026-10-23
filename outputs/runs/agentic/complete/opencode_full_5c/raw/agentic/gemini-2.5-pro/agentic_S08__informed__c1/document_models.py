from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None


class Invoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []
    raw_fields: Dict[str, Any] = {}


class ReceiptItem(BaseModel):
    item_name: Optional[str] = None
    item_quantity: Optional[float] = None
    item_price: Optional[float] = None


class Receipt(BaseModel):
    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None

    items: List[ReceiptItem] = []
    raw_fields: Dict[str, Any] = {}


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    line_items: List[Dict[str, Any]] = []
    source_document_type: str
    source_document_id: str
