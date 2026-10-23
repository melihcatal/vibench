import dataclasses
from typing import List, Optional, Dict, Any


@dataclasses.dataclass
class LineItem:
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None


@dataclasses.dataclass
class ExpenseDocument:
    document_type: Optional[str] = None
    vendor_name: Optional[str] = None
    document_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = dataclasses.field(default_factory=list)
    merchant_name: Optional[str] = None
    notes: Optional[str] = None
    raw_extraction_data: Dict[str, Any] = dataclasses.field(default_factory=dict)
    validation_status: Optional[str] = None
