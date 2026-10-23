from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class DocumentPayload(BaseModel):
    document_bytes: bytes
    mime_type: str

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None

class ExtractedInvoice(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[float] = None
    line_items: List[LineItem] = Field(default_factory=list)
    currency: Optional[str] = None # Added for normalization

class ExtractedReceipt(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[float] = None
    total: Optional[float] = None
    items: List[LineItem] = Field(default_factory=list)
    currency: Optional[str] = None # Added for normalization

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)
    raw_extraction: Dict[str, Any] = Field(default_factory=dict)

class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str] = Field(default_factory=list)
    low_confidence_fields: Dict[str, float] = Field(default_factory=dict)
    message: str
