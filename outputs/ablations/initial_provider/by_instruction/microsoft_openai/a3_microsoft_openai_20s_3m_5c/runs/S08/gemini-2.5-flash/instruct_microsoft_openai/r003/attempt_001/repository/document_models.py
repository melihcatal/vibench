from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import date

class LineItem(BaseModel):
    description: str
    quantity: float
    unit_price: float
    total: float

class ExtractedInvoice(BaseModel):
    vendor: str
    date: date
    total: float
    line_items: List[LineItem] = []

class ExtractedReceipt(BaseModel):
    merchant: str
    tax: Optional[float]
    total: float
    items: List[Dict[str, Any]] = []

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: str
    transaction_date: date
    total_amount: float
    currency: str = "USD"
    line_items: List[LineItem] = []
    notes: Optional[str] = None
    original_data: Dict[str, Any] = Field(default_factory=dict)
    validation_status: str = "pending"
    confidence_score: Optional[float] = None
