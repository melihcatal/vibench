from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class DocumentType(str, Enum):
    INVOICE = "invoice"
    RECEIPT = "receipt"


class LineItem(BaseModel):
    description: str = Field(..., min_length=1)
    quantity: Optional[float] = Field(None, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    amount: float = Field(..., ge=0)


class NormalizedExpense(BaseModel):
    document_type: DocumentType
    merchant_vendor: str = Field(..., min_length=1)
    date: datetime
    subtotal: Optional[float] = Field(None, ge=0)
    tax: Optional[float] = Field(None, ge=0)
    total: float = Field(..., ge=0)
    currency: str = "USD"
    line_items: List[LineItem] = Field(default_factory=list)
    confidence: Optional[Dict[str, float]] = Field(default_factory=dict)
