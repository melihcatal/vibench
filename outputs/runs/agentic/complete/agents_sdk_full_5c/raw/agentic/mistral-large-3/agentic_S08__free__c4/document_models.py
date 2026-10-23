from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class LineItem(BaseModel):
    description: Optional[str] = None
    amount: Optional[str] = None


class InvoiceFields(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)


class ReceiptItem(BaseModel):
    name: Optional[str] = None
    price: Optional[str] = None


class ReceiptFields(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[ReceiptItem] = Field(default_factory=list)


class NormalizedExpense(BaseModel):
    expense_type: str
    vendor: Optional[str] = None
    date: Optional[str] = None
    amount: Optional[str] = None
    line_items: List[Dict[str, Optional[str]]] = Field(default_factory=list)
    tax: Optional[str] = None
    merchant: Optional[str] = None


class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str] = Field(default_factory=list)
    low_confidence_fields: List[str] = Field(default_factory=list)