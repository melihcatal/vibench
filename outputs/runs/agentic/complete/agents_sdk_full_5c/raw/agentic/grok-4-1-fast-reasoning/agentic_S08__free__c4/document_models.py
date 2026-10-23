from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class InvoiceFields(BaseModel):
    vendor: str = Field(..., description="Vendor name")
    date: str
    total: float
    line_items: List[LineItem] = []
    confidence: Dict[str, float] = {}

class ReceiptFields(BaseModel):
    merchant: str = Field(..., description="Merchant name")
    date: Optional[str] = None
    tax: Optional[float] = None
    total: float
    items: List[str] = []
    confidence: Dict[str, float] = {}

class NormalizedExpense(BaseModel):
    document_type: str  # 'invoice' or 'receipt'
    vendor_merchant: str
    date: str
    tax: Optional[float] = None
    total: float
    line_items: List[LineItem] = []
    confidence: Dict[str, float] = {}