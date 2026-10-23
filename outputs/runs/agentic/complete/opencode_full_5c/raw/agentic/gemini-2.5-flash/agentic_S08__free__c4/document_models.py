from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class DocumentExtractionRequest(BaseModel):
    document_content: str  # Base64 encoded document content
    mime_type: str


class ExtractedInvoiceFields(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_text: Optional[str] = None


class ExtractedReceiptFields(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_text: Optional[str] = None


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    tax_amount: Optional[float] = None
    invoice_date: Optional[str] = None
    raw_document_text: Optional[str] = None
    validation_status: str = "pending"
    confidence_scores: Dict[str, float] = Field(default_factory=dict)


class FieldValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    confidence: Optional[float] = None


class DocumentValidationResult(BaseModel):
    is_valid: bool
    validation_errors: List[FieldValidationResult] = Field(default_factory=list)
