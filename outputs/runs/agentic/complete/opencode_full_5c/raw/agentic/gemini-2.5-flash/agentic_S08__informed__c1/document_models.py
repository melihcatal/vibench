from pydantic import BaseModel, Field
from typing import List, Optional


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    currency: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_order: Optional[str] = None


class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    currency: Optional[str] = None


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    notes: Optional[str] = None
    confidence_score: Optional[float] = None


class FieldValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    confidence_score: Optional[float] = None
