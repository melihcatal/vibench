from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentPayload(BaseModel):
    document_bytes: bytes
    mime_type: str

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None

class NormalizedExpense(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[str] = None
    currency: Optional[str] = None
    tax_amount: Optional[str] = None
    merchant_name: Optional[str] = None
    line_items: List[LineItem] = []
    original_data: Dict[str, Any] = Field(default_factory=dict)

class InvoiceExtractionResult(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[LineItem] = []

class ReceiptExtractionResult(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[LineItem] = []
