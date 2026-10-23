from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None

class ReceiptItem(BaseModel):
    name: str
    price: Optional[float] = None

class InvoiceFields(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem] = []
    confidence: Optional[float] = None

class ReceiptFields(BaseModel):
    merchant: str
    tax: Optional[float] = None
    total: float
    items: List[ReceiptItem] = []
    confidence: Optional[float] = None

class NormalizedExpense(BaseModel):
    expense_id: str = Field(..., description="Unique ID")
    type: str  # 'invoice' or 'receipt'
    vendor_or_merchant: str
    date: str
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: float
    items: List[Dict[str, Any]]
    raw_extraction: Optional[Dict[str, Any]] = None

class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str]
    issues: List[str]
    overall_confidence: float