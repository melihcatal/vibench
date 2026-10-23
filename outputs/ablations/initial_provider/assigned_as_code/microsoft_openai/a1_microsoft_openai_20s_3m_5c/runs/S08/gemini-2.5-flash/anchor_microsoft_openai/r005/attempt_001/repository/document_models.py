from pydantic import BaseModel, Field
from typing import List, Optional


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None  # For invoices
    price: Optional[str] = None  # For receipts


class ExpenseRecord(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[str] = None
    tax_amount: Optional[str] = None
    currency: Optional[str] = None
    document_type: Optional[str] = None  # e.g., 'invoice', 'receipt'
    line_items: List[LineItem] = Field(default_factory=list)
    raw_extraction: Optional[dict] = None


class DocumentExtractionPayload(BaseModel):
    document_bytes: bytes
    mime_type: str

