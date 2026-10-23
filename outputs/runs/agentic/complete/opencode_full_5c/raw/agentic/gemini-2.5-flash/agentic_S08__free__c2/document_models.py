from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class LineItem:
    description: str
    amount: float
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


@dataclass
class NormalizedExpense:
    transaction_type: str  # "invoice" or "receipt"
    vendor_name: str
    transaction_date: str  # YYYY-MM-DD
    total_amount: float
    currency: str = "USD"
    line_items: List[LineItem] = field(default_factory=list)
    tax_amount: Optional[float] = None
    notes: Optional[str] = None
    original_data: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class DocumentValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[str] = field(default_factory=list)
    message: str = ""
