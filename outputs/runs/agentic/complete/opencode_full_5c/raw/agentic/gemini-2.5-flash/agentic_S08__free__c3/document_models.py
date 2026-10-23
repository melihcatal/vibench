from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractedField(BaseModel):
    name: str
    value: Optional[str] = None
    confidence: float = 0.0


class ExtractedDocument(BaseModel):
    document_type: str
    fields: List[ExtractedField] = []


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class NormalizedExpense(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = []
    original_document_type: Optional[str] = None
    validation_status: str = "PENDING"
