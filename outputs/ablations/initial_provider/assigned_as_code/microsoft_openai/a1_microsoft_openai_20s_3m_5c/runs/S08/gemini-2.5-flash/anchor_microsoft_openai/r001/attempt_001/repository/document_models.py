from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None

class ExtractedDocument(BaseModel):
    vendor_name: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    merchant_name: Optional[str] = None
    tax: Optional[float] = None
    items: List[LineItem] = Field(default_factory=list)
    # Add a confidence score to each field if available from the extraction service
    confidence: Dict[str, float] = Field(default_factory=dict)

class NormalizedExpense(BaseModel):
    transaction_date: Optional[str] = None
    vendor: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = "USD"
    category: Optional[str] = "Uncategorized"
    description: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    original_document_type: Optional[str] = None # e.g., "invoice", "receipt"
