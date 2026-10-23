from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    total: Optional[float] = None

@dataclass
class NormalizedExpenseRecord:
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_extraction: Dict[str, Any] = field(default_factory=dict)
    validation_results: Dict[str, Any] = field(default_factory=dict)
