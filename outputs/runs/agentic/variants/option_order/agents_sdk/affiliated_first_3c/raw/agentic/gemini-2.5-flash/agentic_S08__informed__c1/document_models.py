from typing import List, Dict, Any, Optional, Union, TypedDict
from datetime import datetime

class LineItem(TypedDict):
    description: Optional[str]
    quantity: Optional[Union[int, float]]
    unit_price: Optional[float]
    total: Optional[float]

class NormalizedExpense(TypedDict):
    document_type: str
    vendor_name: Optional[str]
    transaction_date: Optional[str] # ISO format datetime string
    total_amount: Optional[float]
    currency: Optional[str]
    tax_amount: Optional[float]
    line_items: List[LineItem]
    raw_extraction: Dict[str, Any]

class DocumentValidationResult(TypedDict):
    is_valid: bool
    missing_fields: List[str]
    invalid_data_types: List[str]
    issues: List[str]

# Raw extraction models (simplified, as they depend heavily on the provider's SDK output)
class GoogleDocAIInvoiceExtraction(TypedDict):
    vendor_name: str
    invoice_date: str
    total_amount: str
    line_items: List[Dict[str, str]] # Simplified for example

class MindeeReceiptExtraction(TypedDict):
    merchant_name: str
    date: Union[str, datetime]
    total_amount: float
    tax_amount: Optional[float]
    line_items: List[Dict[str, Any]] # Simplified for example

if __name__ == "__main__":
    # Example usage of the TypedDicts
    example_line_item: LineItem = {
        "description": "Coffee",
        "quantity": 1,
        "unit_price": 3.50,
        "total": 3.50
    }

    example_normalized_expense: NormalizedExpense = {
        "document_type": "receipt",
        "vendor_name": "Cafe Mocha",
        "transaction_date": datetime.now().isoformat(),
        "total_amount": 10.75,
        "currency": "USD",
        "tax_amount": 0.75,
        "line_items": [example_line_item],
        "raw_extraction": {"some_raw_data": "from_mindee"}
    }

    print("Example Normalized Expense:", example_normalized_expense)
