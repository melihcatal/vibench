from pydantic import BaseModel, Field
from typing import List, Optional


class ConfidenceField(BaseModel):
    value: str
    confidence: float = Field(ge=0.0, le=1.0)


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: float


class ExpenseRecord(BaseModel):
    doc_type: str  # "invoice" or "receipt"
    vendor_or_merchant: str
    date: str  # YYYY-MM-DD
    total: float
    tax: Optional[float] = None
    line_items: List[LineItem]
