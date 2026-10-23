from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedField(BaseModel):
    name: str
    value: Optional[str]
    confidence: Optional[float]

class LineItem(BaseModel):
    description: Optional[str]
    quantity: Optional[str]
    amount: Optional[str]

class ExtractedDocument(BaseModel):
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    tax: Optional[str] = None
    items: List[LineItem] = Field(default_factory=list)
    line_items: List[LineItem] = Field(default_factory=list) # For invoices

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[dict] = Field(default_factory=list)
    notes: Optional[str] = None
