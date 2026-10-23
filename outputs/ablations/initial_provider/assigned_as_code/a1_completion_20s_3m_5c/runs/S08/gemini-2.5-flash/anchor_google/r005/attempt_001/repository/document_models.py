from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None


class ExpenseRecord(BaseModel):
    document_type: str = Field(..., description="Type of document, e.g., 'invoice' or 'receipt'")
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = []
    raw_extraction: Dict[str, Any] = Field(..., description="Raw data extracted from the document")