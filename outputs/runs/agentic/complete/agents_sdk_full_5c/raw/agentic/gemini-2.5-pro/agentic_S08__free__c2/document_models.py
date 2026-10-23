from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class ParsedLineItem(BaseModel):
    description: Optional[str] = None
    amount: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[str] = None

class ParsedInvoice(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[ParsedLineItem] = []

class ParsedReceipt(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[Dict[str, Any]] = []

class NormalizedExpense(BaseModel):
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str
    line_items: List[Dict[str, Any]]

class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
