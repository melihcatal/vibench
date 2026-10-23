from typing import List, Optional, Dict, Union
from pydantic import BaseModel, Field
from datetime import datetime

class LineItem(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: Optional[float] = Field(None, description="Quantity")
    unit_price: Optional[float] = Field(None, description="Unit price")
    amount: float = Field(..., description="Line total")

class DocumentFields(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor or merchant name")
    merchant: Optional[str] = Field(None, description="Merchant name for receipts")
    date: Optional[str] = Field(None, description="Invoice or transaction date")
    total: Optional[float] = Field(None, description="Total amount")
    tax: Optional[float] = Field(None, description="Tax amount")
    line_items: List[LineItem] = Field(default_factory=list, description="List of line items")
    confidence: Dict[str, float] = Field(default_factory=dict, description="Confidence scores")

class NormalizedExpense(BaseModel):
    document_type: str = Field(..., description="'invoice' or 'receipt'")
    vendor_name: str = Field(..., description="Standardized vendor/merchant name")
    transaction_date: str = Field(..., description="ISO date YYYY-MM-DD")
    total_amount: float = Field(..., description="Total amount")
    tax_amount: Optional[float] = Field(None, description="Tax amount")
    line_items: List[LineItem] = Field(default_factory=list)
    raw_confidence: Dict[str, float] = Field(default_factory=dict)