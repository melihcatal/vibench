from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class NormalizedExpense(BaseModel):
    merchant: str = Field(..., min_length=1)
    date: str
    total: float = Field(..., gt=0)
    tax: Optional[float] = None
    items: List[LineItem] = []
