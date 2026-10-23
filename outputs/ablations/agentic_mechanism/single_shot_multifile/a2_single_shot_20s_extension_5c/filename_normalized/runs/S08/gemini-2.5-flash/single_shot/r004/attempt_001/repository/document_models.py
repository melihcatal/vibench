from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class InvoiceLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class ExtractedInvoiceFields(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[InvoiceLineItem] = Field(default_factory=list)
    raw_text: Optional[str] = None

class ReceiptItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class ExtractedReceiptFields(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    items: List[ReceiptItem] = Field(default_factory=list)
    raw_text: Optional[str] = None

class NormalizedExpense(BaseModel):
    document_type: str
    primary_vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = "Uncategorized"
    line_items: List[Dict[str, Any]] = Field(default_factory=list)
    notes: Optional[str] = None
    original_extracted_data: Dict[str, Any]

class FieldValidation(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    confidence_score: Optional[float] = None

class DocumentValidationResult(BaseModel):
    is_document_valid: bool
    overall_message: Optional[str] = None
    field_validations: List[FieldValidation] = Field(default_factory=list)
    required_fields_missing: List[str] = Field(default_factory=list)
    low_confidence_fields: List[str] = Field(default_factory=list)
