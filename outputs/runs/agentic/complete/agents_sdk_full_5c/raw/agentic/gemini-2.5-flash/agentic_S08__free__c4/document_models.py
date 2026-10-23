from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None # ISO format
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = []
    notes: Optional[str] = None

class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None # ISO format
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = []

class NormalizedExpense(BaseModel):
    document_type: str # 'invoice' or 'receipt'
    transaction_date: Optional[str] = None # ISO format, prefer invoice_date/transaction_date
    vendor_merchant_name: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None # Only applicable for receipts, or if explicitly found on invoice
    line_items: List[LineItem] = []
    notes: Optional[str] = None
    source_document_uri: Optional[str] = None
    validation_scores: Dict[str, float] = Field(default_factory=dict)
