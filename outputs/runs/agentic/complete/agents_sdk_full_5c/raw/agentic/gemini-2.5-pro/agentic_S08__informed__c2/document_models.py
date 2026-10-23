
from pydantic import BaseModel, Field
from typing import List, Optional, Union
from datetime import date

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

class NormalizedExpense(BaseModel):
    # For invoices
    vendor_name: Optional[str] = None
    invoice_id: Optional[str] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    invoice_total: Optional[float] = None
    
    # For receipts
    merchant_name: Optional[str] = None
    transaction_date: Optional[date] = None
    tax: Optional[float] = None
    total: Optional[float] = None

    # Common
    line_items: List[LineItem] = Field(default_factory=list)
    currency_symbol: Optional[str] = None
    raw_text: Optional[str] = None
