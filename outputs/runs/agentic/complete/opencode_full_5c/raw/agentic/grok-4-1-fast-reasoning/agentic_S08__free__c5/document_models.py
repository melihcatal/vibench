from typing import TypedDict, Dict, Any, List, Optional


class InvoiceFields(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[Dict[str, Any]]


class ReceiptFields(TypedDict):
    merchant: str
    tax: float
    total: float
    items: List[Dict[str, Any]]


class NormalizedExpense(TypedDict):
    document_type: str
    vendor_merchant: str
    date: str
    total: float
    tax: Optional[float]
    line_items: List[Dict[str, Any]]
    confidence: Optional[Dict[str, float]]


class ValidationResult(TypedDict):
    is_valid: bool
    issues: List[str]
    overall_confidence: float
