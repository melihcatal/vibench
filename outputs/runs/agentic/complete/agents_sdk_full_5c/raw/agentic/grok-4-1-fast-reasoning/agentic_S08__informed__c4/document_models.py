from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LineItem(BaseModel):
    description: str = Field(..., description='Item description')
    quantity: Optional[float] = Field(None, ge=0)
    unit_price: Optional[float] = Field(None, ge=0)
    amount: float = Field(..., ge=0)
    confidence: Optional[float] = Field(None, ge=0, le=1)

class NormalizedExpense(BaseModel):
    merchant_name: str
    transaction_date: str
    total_amount: float = Field(..., ge=0)
    tax_amount: Optional[float] = Field(None, ge=0)
    line_items: List[LineItem] = Field(default_factory=list)