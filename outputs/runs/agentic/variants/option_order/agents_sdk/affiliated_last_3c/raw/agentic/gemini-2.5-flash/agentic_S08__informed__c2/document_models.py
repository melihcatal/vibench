from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class NormalizedExpense(BaseModel):
    document_type: str = Field(..., description="Type of the document, e.g., 'invoice' or 'receipt'")
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None # ISO 8601 format
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = []
    confidence_scores: Dict[str, float] = Field(default_factory=dict, description="Confidence scores for extracted fields")
    raw_document_path: Optional[str] = None
    notes: Optional[str] = None # For additional vendor notes or descriptions
