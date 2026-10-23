from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class DocumentPayload(BaseModel):
    document_bytes: bytes
    mime_type: str

class ExtractedField(BaseModel):
    type: str
    value: Optional[str] = None
    confidence: Optional[float] = None

class ExtractedItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None
    confidence: Optional[float] = None

class InvoiceExtractionResult(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[ExtractedItem] = []

class ReceiptExtractionResult(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[ExtractedItem] = []

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[Dict[str, Any]] = []
    original_data: Dict[str, Any]
    validation_errors: List[str] = []
    confidence_scores: Dict[str, float] = {}

class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    confidence: Optional[float] = None

class DocumentValidationResponse(BaseModel):
    document_type: str
    is_valid: bool
    validation_results: List[ValidationResult]