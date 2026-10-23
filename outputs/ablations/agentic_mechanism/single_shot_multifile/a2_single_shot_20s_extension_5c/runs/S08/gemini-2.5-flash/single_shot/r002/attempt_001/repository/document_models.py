from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentInput(BaseModel):
    base64_image: str
    mime_type: str # e.g., 'application/pdf', 'image/jpeg', 'image/png'

class InvoiceLineItem(BaseModel):
    description: str = ""
    quantity: int = 0
    unit_price: float = 0.0
    total: float = 0.0

class InvoiceFields(BaseModel):
    vendor_name: str = ""
    invoice_date: str = ""
    total_amount: float = 0.0
    currency: str = ""
    line_items: List[InvoiceLineItem] = Field(default_factory=list)

class ReceiptItem(BaseModel):
    description: str = ""
    price: float = 0.0
    quantity: int = 0
    total: float = 0.0

class ReceiptFields(BaseModel):
    merchant_name: str = ""
    tax_amount: float = 0.0
    total_amount: float = 0.0
    currency: str = ""
    items: List[ReceiptItem] = Field(default_factory=list)

class NormalizedExpenseLineItem(BaseModel):
    description: str
    quantity: float # Can be non-integer for services, etc.
    unit_price: float
    total: float

class NormalizedExpense(BaseModel):
    transaction_type: str # 'invoice' or 'receipt'
    vendor_name: str
    transaction_date: str # YYYY-MM-DD
    total_amount: float
    currency: str # ISO 4217 code, e.g., USD
    tax_amount: Optional[float] = None
    line_items: List[NormalizedExpenseLineItem] = Field(default_factory=list)
    notes: Optional[str] = None

class DocumentValidationResult(BaseModel):
    is_valid: bool
    validation_errors: List[str] = Field(default_factory=list)
