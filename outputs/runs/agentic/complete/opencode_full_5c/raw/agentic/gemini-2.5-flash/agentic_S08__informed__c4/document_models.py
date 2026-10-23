import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class NormalizedExpense(BaseModel):
    document_type: str = Field(
        ..., description="Type of document, e.g., 'invoice' or 'receipt'"
    )
    vendor_name: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = []
    raw_text: Optional[str] = None
    document_id: Optional[str] = None
