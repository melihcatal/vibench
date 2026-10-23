from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field

@dataclass
class LineItem:
    description: str
    amount: float
    quantity: Optional[int] = None
    unit_price: Optional[float] = None

@dataclass
class ExtractedDocumentFields:
    document_type: str
    vendor_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    currency: Optional[str] = None
    line_items: List[LineItem] = field(default_factory=list)
    tax_amount: Optional[float] = None
    notes: Optional[str] = None
    confidence_scores: Dict[str, float] = field(default_factory=dict)
    raw_extraction_data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationResult:
    is_valid: bool
    missing_fields: List[str] = field(default_factory=list)
    low_confidence_fields: List[Dict[str, Any]] = field(default_factory=list)

if __name__ == '__main__':
    # Example Usage
    item1 = LineItem(description="Laptop", amount=1200.00, quantity=1)
    item2 = LineItem(description="Mouse", amount=25.50, quantity=2)

    invoice_data = ExtractedDocumentFields(
        document_type="invoice",
        vendor_name="Tech Store Inc.",
        transaction_date="2023-10-27",
        total_amount=1251.00,
        currency="USD",
        line_items=[item1, item2],
        tax_amount=0.0,
        confidence_scores={
            "vendor_name": 0.98,
            "total_amount": 0.92
        }
    )

    print(f"Invoice Data: {invoice_data}")
    print(f"First Line Item: {invoice_data.line_items[0].description}, Amount: {invoice_data.line_items[0].amount}")

    validation_output = ValidationResult(
        is_valid=False,
        missing_fields=["notes"],
        low_confidence_fields=[{"field": "total_amount", "score": 0.65}]
    )
    print(f"Validation Result: {validation_output}")
