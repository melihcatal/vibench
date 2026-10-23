from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: Optional[float] = Field(None, description="Quantity")
    unit_price: Optional[float] = Field(None, description="Unit price")
    amount: float = Field(..., description="Line item amount")


class ExtractedInvoice(BaseModel):
    vendor: str
    invoice_date: str
    total: float
    line_items: List[LineItem] = Field(default_factory=list)
    confidences: Dict[str, float] = Field(default_factory=dict)


class ExtractedReceipt(BaseModel):
    merchant: str
    tax: Optional[float] = None
    total: float
    items: List[str] = Field(default_factory=list)
    confidences: Dict[str, float] = Field(default_factory=dict)


class NormalizedExpense(BaseModel):
    document_type: str
    payee: str
    date: str
    subtotal: Optional[float] = None
    tax: Optional[float] = None
    total: float
    line_items: List[LineItem] = Field(default_factory=list)
    confidence: float


class ValidationResult(BaseModel):
    is_valid: bool
    issues: List[str] = Field(default_factory=list)
    overall_confidence: float
