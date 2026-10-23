import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


class DocumentExtractionRequest(BaseModel):
    document_content: str  # Base64 encoded document content
    document_type: str  # e.g., "invoice", "receipt"


class InvoiceExtractionResult(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[datetime.date] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []
    currency: Optional[str] = None
    raw_response: Dict[str, Any] = Field(default_factory=dict)


class ReceiptExtractionResult(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []
    currency: Optional[str] = None
    raw_response: Dict[str, Any] = Field(default_factory=dict)


class NormalizedExpense(BaseModel):
    document_type: str
    vendor_merchant_name: Optional[str] = None
    transaction_date: Optional[datetime.date] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = []
    notes: Optional[str] = None
    confidence_scores: Dict[str, float] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: List[str] = []
    low_confidence_fields: Dict[str, float] = Field(default_factory=dict)
