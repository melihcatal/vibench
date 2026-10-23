import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class LineItem:
    description: str
    amount: float
    quantity: Optional[float] = None
    unit_price: Optional[float] = None


@dataclass
class ExpenseRecord:
    transaction_id: str
    document_type: str  # "invoice" or "receipt"
    vendor_name: str
    transaction_date: str
    total_amount: float
    currency: str = "USD"
    tax_amount: Optional[float] = None
    line_items: List[LineItem] = field(default_factory=list)
    raw_extraction_data: Dict[str, Any] = field(default_factory=dict)
    notes: Optional[str] = None

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    @classmethod
    def from_json(cls, json_string):
        data = json.loads(json_string)
        line_items = [LineItem(**item) for item in data.pop("line_items", [])]
        return cls(line_items=line_items, **data)
