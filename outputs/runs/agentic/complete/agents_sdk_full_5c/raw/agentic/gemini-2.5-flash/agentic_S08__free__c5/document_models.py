from pydantic import BaseModel, Field
from typing import List, Optional, Any, Dict

class LineItem(BaseModel):
    description: str = Field(default="", description="Description of the line item.")
    quantity: float = Field(default=0.0, description="Quantity of the item.")
    unit_price: float = Field(default=0.0, description="Unit price of the item.")
    amount: float = Field(default=0.0, description="Total amount for the line item.")

class NormalizedExpense(BaseModel):
    document_type: str = Field(..., description="Type of the document (e.g., invoice, receipt).")
    vendor_name: str = Field(default="", description="Name of the vendor/merchant.")
    transaction_date: str = Field(default="", description="Date of the transaction in YYYY-MM-DD format.")
    total_amount: float = Field(default=0.0, description="Total amount of the expense.")
    tax_amount: float = Field(default=0.0, description="Total tax amount.")
    currency: str = Field(default="USD", description="Currency of the transaction.")
    line_items: List[LineItem] = Field(default_factory=list, description="List of line items.")
    raw_extraction: Optional[Dict[str, Any]] = Field(default=None, description="Original raw extracted data.")
    notes: Optional[str] = Field(default=None, description="Any additional notes or memo from the document.")

class ExpenseRecord(NormalizedExpense):
    record_id: Optional[str] = Field(default=None, description="Unique ID for the stored expense record.")
    validation_status: Dict[str, Any] = Field(default_factory=dict, description="Result of validation process.")
    summary: Optional[str] = Field(default=None, description="Summary generated for the invoice.")
    safety_moderation: Optional[Dict[str, Any]] = Field(default=None, description="Result of safety moderation for vendor notes.")
    translated_notes: Optional[str] = Field(default=None, description="Translated version of the invoice notes.")

if __name__ == '__main__':
    # Example Usage
    item1 = LineItem(description="Laptop", quantity=1.0, unit_price=1200.00, amount=1200.00)
    item2 = LineItem(description="Mouse", quantity=2.0, unit_price=25.00, amount=50.00)

    expense_data = NormalizedExpense(
        document_type="invoice",
        vendor_name="Tech Solutions Inc.",
        transaction_date="2023-10-27",
        total_amount=1250.00,
        tax_amount=75.00,
        line_items=[item1, item2],
        raw_extraction={"some_raw_field": "raw value"}
    )

    print(expense_data.model_dump_json(indent=2))

    expense_record_data = ExpenseRecord(
        **expense_data.model_dump(),
        record_id="exp_123",
        validation_status={"is_valid": True, "missing_fields": []}
    )

    print(expense_record_data.model_dump_json(indent=2))
