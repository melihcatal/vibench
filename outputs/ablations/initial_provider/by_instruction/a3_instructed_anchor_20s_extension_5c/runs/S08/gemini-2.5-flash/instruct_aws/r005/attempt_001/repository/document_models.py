from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    price: Optional[str] = None
    quantity: Optional[str] = None

class ExtractedExpense(BaseModel):
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    document_date: Optional[str] = None
    tax_amount: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    # Add a generic field for any other extracted data not explicitly mapped
    additional_data: Dict[str, Any] = Field(default_factory=dict)
