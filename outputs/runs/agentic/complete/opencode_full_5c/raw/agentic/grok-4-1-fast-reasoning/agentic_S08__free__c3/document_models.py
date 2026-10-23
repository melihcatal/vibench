from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = Field(default=0.0)
    unit_price: Optional[float] = Field(default=0.0)
    total: float


class RawInvoice(BaseModel):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem] = []


class RawReceipt(BaseModel):
    merchant: str
    tax: Optional[float] = Field(default=None)
    total: float
    items: List[str] = []


class NormalizedExpense(BaseModel):
    doc_type: str
    vendor: str
    date: str
    subtotal: Optional[float] = Field(default=None)
    tax: Optional[float] = Field(default=None)
    total: float
    line_items: List[Dict[str, Any]] = []
    confidence: float = Field(ge=0.0, le=1.0)


class ValidationResult(BaseModel):
    is_valid: bool
    confidence: float
    issues: List[str] = []
