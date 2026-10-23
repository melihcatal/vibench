from typing import List, Dict, Optional
from pydantic import BaseModel


class InvoiceFields(BaseModel):
    vendor: Optional[str]
    date: Optional[str]
    total: Optional[float]
    line_items: List[Dict[str, Optional[float]]]
    confidence: float


class ReceiptFields(BaseModel):
    merchant: Optional[str]
    tax: Optional[float]
    total: Optional[float]
    items: List[Dict[str, Optional[str]]]
    confidence: float


class NormalizedExpense(BaseModel):
    vendor: Optional[str]
    date: Optional[str]
    amount: float
    currency: str
    items: List[Dict[str, Optional[float]]]
    document_type: str
    confidence: float