from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import date


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: float
    confidence: Optional[float] = None


class InvoiceFields(BaseModel):
    vendor: str
    date: date
    total: float
    line_items: List[LineItem]
    confidence: Optional[Dict[str, float]] = {}


class ReceiptFields(BaseModel):
    merchant: str
    tax: Optional[float] = None
    total: float
    items: List[str]
    confidence: Optional[Dict[str, float]] = {}


class NormalizedExpense(BaseModel):
    type: str
    vendor_or_merchant: str
    date: date
    total: float
    tax: Optional[float] = None
    line_items: List[Dict[str, Any]]
    confidence: Optional[Dict[str, float]] = None


class ValidationResult(BaseModel):
    valid: bool
    errors: List[str] = []
    avg_confidence: Optional[float] = None
