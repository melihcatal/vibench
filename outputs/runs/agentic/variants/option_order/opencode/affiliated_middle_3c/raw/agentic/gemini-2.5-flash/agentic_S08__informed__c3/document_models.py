from pydantic import BaseModel, Field, conlist
from typing import List, Optional
from datetime import date


class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total_price: float


class NormalizedExpense(BaseModel):
    vendor_name: str
    transaction_date: date
    total_amount: float
    currency: str
    tax_amount: Optional[float] = None
    line_items: conlist(LineItem, min_length=0) = []
    document_type: str = "unknown"
    notes: Optional[str] = None
    confidence_vendor: float = Field(..., ge=0, le=1)
    confidence_date: float = Field(..., ge=0, le=1)
    confidence_total: float = Field(..., ge=0, le=1)
