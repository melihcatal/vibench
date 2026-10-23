from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class DocumentExtractionRequest(BaseModel):
    document_bytes: bytes
    file_name: Optional[str] = None
    file_type: Optional[str] = None

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None

class InvoiceFields(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[LineItem] = []

class ReceiptFields(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[LineItem] = []

class ExtractedDocument(BaseModel):
    invoice_fields: Optional[InvoiceFields] = None
    receipt_fields: Optional[ReceiptFields] = None

class NormalizedExpense(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[Dict[str, Any]] = []
    category: Optional[str] = None
    document_type: Optional[str] = None
    confidence_scores: Dict[str, float] = {}

class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None

class DocumentValidationResponse(BaseModel):
    document_id: str
    overall_valid: bool
    validation_results: List[ValidationResult]
