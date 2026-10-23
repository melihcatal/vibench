from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

class ExtractedInvoice(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: Optional[List[LineItem]] = None
    confidence: Optional[Dict[str, float]] = None

class ExtractedReceipt(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    items: Optional[List[str]] = None
    confidence: Optional[Dict[str, float]] = None

class NormalizedExpense(BaseModel):
    type: str  # 'invoice' or 'receipt'
    vendor_or_merchant: str
    date: str
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: float
    line_items: List[Dict[str, Any]]
