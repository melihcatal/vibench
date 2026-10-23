from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

class NormalizedExpense(BaseModel):
    expense_id: str = Field(..., description="Unique identifier for the expense record.")
    source_file: str
    vendor: Optional[str] = None
    transaction_date: Optional[date] = None
    total: Optional[float] = None
    tax: Optional[float] = None
    line_items: List[LineItem] = []
