from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None

class NormalizedExpense(BaseModel):
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    merchant_name: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    document_type: Optional[str] = None
    confidence_score: Optional[float] = None
    raw_extraction: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None

class DocumentExtractionRequest(BaseModel):
    document_bytes: bytes
    mime_type: str

class ValidationResult(BaseModel):
    is_valid: bool
    reasons: List[str] = Field(default_factory=list)
    confidence_score_pass: bool = False
    required_fields_pass: bool = False

class SummaryRequest(BaseModel):
    expense_data: NormalizedExpense

class TranslationRequest(BaseModel):
    text: str
    target_language_code: str = "en"
    source_language_code: Optional[str] = None

class ModerationRequest(BaseModel):
    text: str

class ExpenseRecord(BaseModel):
    record_id: Optional[str] = None
    normalized_expense: NormalizedExpense
    summary: Optional[str] = None
    moderation_result: Optional[Dict[str, Any]] = None
    translated_notes: Optional[str] = None
    created_at: Optional[str] = None