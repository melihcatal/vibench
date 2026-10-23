from typing import TypedDict, List, Dict, Any, Optional, Union

class LineItem(TypedDict):
    description: str
    quantity: Optional[float]
    unit_price: Optional[float]
    amount: float

class ExtractedInvoice(TypedDict):
    vendor: str
    date: str
    total: float
    line_items: List[LineItem]
    confidence: Dict[str, float]

class ExtractedReceipt(TypedDict):
    merchant: str
    tax: Optional[float]
    total: float
    items: List[Dict[str, Any]]
    confidence: Dict[str, float]

class NormalizedExpense(TypedDict):
    doc_type: str
    entity_name: str
    date: str
    tax: Optional[float]
    total: float
    line_items: List[Dict[str, Any]]
    confidence: Dict[str, float]

class ValidationResult(TypedDict):
    is_valid: bool
    issues: List[str]
    overall_confidence: float
