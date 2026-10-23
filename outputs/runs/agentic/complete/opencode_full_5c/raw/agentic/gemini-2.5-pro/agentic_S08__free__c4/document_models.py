from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class Document(BaseModel):
    content: bytes
    mime_type: str


class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None


class Invoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []


class Receipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    line_items: List[LineItem] = []


class NormalizedExpense(BaseModel):
    vendor: str
    transaction_date: str
    total: float
    line_items: List[Dict[str, Any]]
    category: Optional[str] = "Uncategorized"
    raw_text: Optional[str] = None


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    confidence_scores: Dict[str, float]


class Summary(BaseModel):
    summary_text: str


class SafetyResult(BaseModel):
    is_safe: bool
    categories: Dict[str, float]


class TranslationResult(BaseModel):
    translated_text: str
    source_language: str


class PersistenceResult(BaseModel):
    record_id: str
    success: bool
