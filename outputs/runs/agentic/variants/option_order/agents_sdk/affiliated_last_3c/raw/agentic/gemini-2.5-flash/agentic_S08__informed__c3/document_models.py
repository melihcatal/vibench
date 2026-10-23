from pydantic import BaseModel, Field
from typing import Optional, List

class LineItem(BaseModel):
    description: str
    amount: float
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str]
    invoice_date: Optional[str]
    total_amount: Optional[str]
    line_items: List[dict] = Field(default_factory=list)

class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str]
    total_tax: Optional[float]
    total_amount: Optional[float]
    currency: Optional[str]
    line_items: List[dict] = Field(default_factory=list)

class ExpenseDocument(BaseModel):
    document_type: str
    vendor_name: Optional[str]
    document_date: Optional[str]
    total_amount: Optional[float]
    total_tax: Optional[float] = None
    currency: Optional[str]
    line_items: List[LineItem] = Field(default_factory=list)
    notes: Optional[str] = None
    original_extraction: dict = Field(default_factory=dict)
