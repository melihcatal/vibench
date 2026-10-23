from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class ExtractedField(BaseModel):
    value: Optional[str] = None
    confidence: Optional[float] = None

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None

class DocumentExtractionResponse(BaseModel):
    vendor: ExtractedField
    date: ExtractedField
    total: ExtractedField
    tax: Optional[ExtractedField] = None
    merchant: Optional[ExtractedField] = None
    line_items: List[LineItem] = []

class NormalizedExpense(BaseModel):
    transaction_id: Optional[str] = None
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    line_items: List[Dict[str, Any]] = []
    original_document_type: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None

class ValidationRule(BaseModel):
    field_name: str
    required: bool
    min_confidence: float = 0.8
    data_type: Optional[str] = None # e.g., "string", "number", "date"

class DocumentValidationConfig(BaseModel):
    document_type: str
    rules: List[ValidationRule]
