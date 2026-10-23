from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: float


class InvoiceFields(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem] = []
    confidence: Optional[Dict[str, float]] = None


class ReceiptFields(BaseModel):
    merchant: str
    tax: Optional[float] = None
    total: float
    items: List[str] = []
    confidence: Optional[Dict[str, float]] = None


class NormalizedExpense(BaseModel):
    vendor_merchant: str
    date: str
    total_amount: float
    tax_amount: Optional[float] = None
    items: List[Dict[str, Any]] = []
    confidence: Dict[str, float]
