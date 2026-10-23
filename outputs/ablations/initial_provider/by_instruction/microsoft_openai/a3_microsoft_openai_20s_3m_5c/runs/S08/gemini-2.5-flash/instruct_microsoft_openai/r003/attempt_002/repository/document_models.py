from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class ExtractedInvoiceFields(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)

class ExtractedReceiptFields(BaseModel):
    merchant_name: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[LineItem] = Field(default_factory=list)

class NormalizedExpense(BaseModel):
    document_type: str = Field(..., description="Type of the document, e.g., 'invoice' or 'receipt'")
    vendor_merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    tax_amount: Optional[float] = None
    note: Optional[str] = None
    confidence_score: Optional[float] = None

class DocumentValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str] = Field(default_factory=list)
    low_confidence_fields: List[str] = Field(default_factory=list)
