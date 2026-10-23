from typing import List, Optional
from pydantic import BaseModel, Field

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    amount: Optional[float] = None

class Invoice(BaseModel):
    vendor_name: Optional[str] = Field(None, alias="vendor")
    invoice_date: Optional[str] = Field(None, alias="date")
    total_amount: Optional[float] = Field(None, alias="total")
    line_items: List[LineItem] = []

class ReceiptItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    price: Optional[float] = None
    amount: Optional[float] = None

class Receipt(BaseModel):
    merchant_name: Optional[str] = Field(None, alias="merchant")
    transaction_date: Optional[str] = Field(None, alias="date")
    total_amount: Optional[float] = Field(None, alias="total")
    tax_amount: Optional[float] = Field(None, alias="tax")
    items: List[ReceiptItem] = []

class NormalizedExpense(BaseModel):
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    description: Optional[str] = None
    line_items: List[LineItem] = []
    original_data: dict

class ValidationResult(BaseModel):
    field_name: str
    is_valid: bool
    reason: Optional[str] = None

class DocumentValidation(BaseModel):
    overall_valid: bool
    validation_results: List[ValidationResult]
    confidence_scores: dict

class SummaryResult(BaseModel):
    summary_text: str

class ModerationResult(BaseModel):
    is_safe: bool
    categories: List[str]
    scores: dict

class TranslationResult(BaseModel):
    translated_text: str
