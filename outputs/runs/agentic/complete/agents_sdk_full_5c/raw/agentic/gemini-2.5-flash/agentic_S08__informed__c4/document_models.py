import json
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    amount: Optional[float] = None

class ExpenseDocument(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    merchant_name: Optional[str] = None
    date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    invoice_number: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_response: Dict[str, Any] = Field(default_factory=dict)

class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None
    confidence: Optional[float] = None

class DocumentValidationResponse(BaseModel):
    document_id: str
    is_document_valid: bool
    validation_details: List[ValidationResult]
