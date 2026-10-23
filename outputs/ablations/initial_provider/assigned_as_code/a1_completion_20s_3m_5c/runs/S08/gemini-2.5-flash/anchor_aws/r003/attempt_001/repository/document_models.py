from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None

class ExtractedDocumentFields(BaseModel):
    vendor: Optional[str] = None
    merchant: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    tax: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    items: List[LineItem] = Field(default_factory=list) # For receipts

class DocumentExtractionRequest(BaseModel):
    document_bytes: bytes

class DocumentExtractionResponse(BaseModel):
    invoices: List[ExtractedDocumentFields] = Field(default_factory=list)
    receipts: List[ExtractedDocumentFields] = Field(default_factory=list)

class NormalizedExpense(BaseModel):
    transaction_id: Optional[str] = None
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    raw_extraction: Optional[dict] = None # To store the original extraction response
    validation_status: Optional[str] = None
    confidence_score: Optional[float] = None
    notes: Optional[str] = None
    translated_notes: Optional[str] = None
    safety_moderation_status: Optional[str] = None
