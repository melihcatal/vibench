from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List, Dict, Any

# This file assumes expense data has been extracted using a service like AWS Textract,
# which is our identifiable external provider for the extraction phase.

class Address(BaseModel):
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None

class Merchant(BaseModel):
    name: str
    address: Optional[Address] = None
    phone_number: Optional[str] = None
    website: Optional[str] = None

class LineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: float

class Expense(BaseModel):
    date: date
    merchant: Merchant
    total_amount: float
    currency: str
    category: Optional[str] = None
    line_items: Optional[List[LineItem]] = None
    invoice_number: Optional[str] = None
    payment_method: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = Field(default_factory=dict)

def normalize_expense_data(extracted_data: Dict[str, Any]) -> Expense:
    """
    Normalizes extracted expense fields into a standard JSON schema using Pydantic.
    Assumes `extracted_data` comes from a service like AWS Textract.
    """
    # Example transformation and mapping
    merchant_data = extracted_data.get("merchant", {})
    address_data = merchant_data.get("address", {})

    normalized_address = Address(
        street=address_data.get("street"),
        city=address_data.get("city"),
        state=address_data.get("state"),
        zip_code=address_data.get("zip_code"),
        country=address_data.get("country"),
    )

    normalized_merchant = Merchant(
        name=merchant_data.get("name", "Unknown Merchant"),
        address=normalized_address,
        phone_number=merchant_data.get("phone_number"),
        website=merchant_data.get("website"),
    )

    line_items_data = extracted_data.get("line_items", [])
    normalized_line_items = [
        LineItem(
            description=item.get("description"),
            quantity=item.get("quantity"),
            unit_price=item.get("unit_price"),
            total_amount=item.get("total_amount", 0.0),
        ) for item in line_items_data
    ]

    return Expense(
        date=date.fromisoformat(extracted_data["date"]) if "date" in extracted_data else date.today(),
        merchant=normalized_merchant,
        total_amount=extracted_data.get("total_amount", 0.0),
        currency=extracted_data.get("currency", "USD"),
        category=extracted_data.get("category"),
        line_items=normalized_line_items if normalized_line_items else None,
        invoice_number=extracted_data.get("invoice_number"),
        payment_method=extracted_data.get("payment_method"),
        raw_data=extracted_data # Store original extracted data for debugging/audit
    )

if __name__ == "__main__":
    # Example usage with hypothetical data extracted by AWS Textract
    sample_extracted_data = {
        "date": "2023-10-26",
        "total_amount": 105.75,
        "currency": "EUR",
        "merchant": {
            "name": "Coffee Shop XYZ",
            "address": {
                "street": "123 Main St",
                "city": "Anytown",
                "state": "AS",
                "zip_code": "12345",
                "country": "USA"
            },
            "phone_number": "555-123-4567"
        },
        "line_items": [
            {"description": "Espresso", "quantity": 2, "unit_price": 3.50, "total_amount": 7.00},
            {"description": "Pastry", "quantity": 1, "unit_price": 4.25, "total_amount": 4.25}
        ],
        "category": "Food & Beverage",
        "invoice_number": "INV-2023-001",
        "payment_method": "Credit Card"
    }

    normalized_expense = normalize_expense_data(sample_extracted_data)
    print(normalized_expense.model_dump_json(indent=2))

    # Example with minimal data
    minimal_extracted_data = {
        "date": "2023-10-27",
        "total_amount": 50.00,
        "currency": "USD",
        "merchant": {"name": "Online Store"},
    }
    minimal_normalized_expense = normalize_expense_data(minimal_extracted_data)
    print("\nMinimal Normalized Expense:")
    print(minimal_normalized_expense.model_dump_json(indent=2))
