from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class LineItem(BaseModel):
    description: str
    amount: str


class Item(BaseModel):
    description: str
    price: str


class InvoiceFields(BaseModel):
    vendor: str
    date: str
    total: str
    line_items: List[LineItem]


class ReceiptFields(BaseModel):
    merchant: str
    tax: str
    total: str
    items: List[Item]


class NormalizedExpense(BaseModel):
    expense_type: str
    vendor: Optional[str]
    merchant: Optional[str]
    date: Optional[str]
    total_amount: str
    line_items: List[Dict[str, str]]
    tax_amount: Optional[str]


class ValidatedDocument(BaseModel):
    expense_type: str
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total_amount: str
    line_items: List[Dict[str, str]]
    tax_amount: Optional[str] = None
    confidence_scores: Optional[Dict[str, float]] = None

    @validator('total_amount')
    def validate_total_amount(cls, v):
        if not v.replace('.', '', 1).isdigit():
            raise ValueError('Total amount must be a numeric value')
        return v