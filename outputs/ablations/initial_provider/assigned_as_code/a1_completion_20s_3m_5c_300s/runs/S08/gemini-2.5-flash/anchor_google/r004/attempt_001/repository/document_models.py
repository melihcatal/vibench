from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None


class ExpenseRecord(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    notes: Optional[str] = None


class DocumentConfig(BaseModel):
    project_id: str
    location: str
    processor_id: str
    model_id: Optional[str] = None
    collection_id: Optional[str] = None
