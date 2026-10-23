from __future__ import annotations
from typing import List, Dict, Any

class NormalizedExpense:
    def __init__(
        self,
        vendor_or_merchant: str,
        date: str,
        total: str,
        items: List[Dict[str, Any]],
    ):
        self.vendor_or_merchant = vendor_or_merchant
        self.date = date
        self.total = total
        self.items = items  # List of dicts with at least 'description' and 'price/quantity/unit_price'
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "vendor_or_merchant": self.vendor_or_merchant,
            "date": self.date,
            "total": self.total,
            "items": self.items,
            "schema_version": "1.0",
        }

# Example helper to serialize
serialize_expense = lambda ne: ne.to_dict()
