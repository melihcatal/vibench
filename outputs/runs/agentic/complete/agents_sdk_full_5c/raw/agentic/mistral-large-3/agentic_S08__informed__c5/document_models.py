from pydantic import BaseModel
from typing import Dict, Any, List, Optional


class InvoiceExtractionResponse(BaseModel):
    raw_fields: Dict[str, Any]
    confidence: float
    model_used: str


class ReceiptExtractionResponse(BaseModel):
    raw_fields: Dict[str, Any]
    confidence: float
    model_used: str


class NormalizedExpense(BaseModel):
    vendor_merchant: str
    date: str
    total_amount: float
    tax_amount: float = 0.0
    items: List[Dict[str, Any]] = []


class ValidationResult(BaseModel):
    is_valid: bool
    errors: List[str]
    confidence: float


class ExpenseRecord(BaseModel):
    expense_id: str
    normalized_expense: NormalizedExpense
    metadata: Dict[str, Any]