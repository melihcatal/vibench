from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    invoice_number: Optional[str] = None
    purchase_order_number: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_text: Optional[str] = None
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
