from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None

class NormalizedExpense(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    document_type: Optional[str] = None
    raw_extraction_data: Dict[str, Any] = Field(default_factory=dict)
    validation_results: Dict[str, Any] = Field(default_factory=dict)
    summary: Optional[str] = None
    safety_scores: Optional[Dict[str, Any]] = None
    translated_notes: Optional[Dict[str, Any]] = None
