from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(default=None)
    quantity: Optional[float] = Field(default=None)
    unit_price: Optional[float] = Field(default=None)
    amount: Optional[float] = Field(default=None)


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = Field(default=None)
    invoice_date: Optional[str] = Field(default=None)
    due_date: Optional[str] = Field(default=None)
    total: Optional[float] = Field(default=None)
    tax: Optional[float] = Field(default=None)
    line_items: List[LineItem] = Field(default_factory=list)
    confidence: Dict[str, float] = Field(default_factory=dict)


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = Field(default=None)
    transaction_date: Optional[str] = Field(default=None)
    total: Optional[float] = Field(default=None)
    tax: Optional[float] = Field(default=None)
    line_items: List[LineItem] = Field(default_factory=list)
    confidence: Dict[str, float] = Field(default_factory=dict)


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_or_merchant: str
    date: str
    total: float
    tax: Optional[float] = Field(default=None)
    line_items: List[LineItem] = Field(default_factory=list)
    confidence: Dict[str, float] = Field(default_factory=dict)
