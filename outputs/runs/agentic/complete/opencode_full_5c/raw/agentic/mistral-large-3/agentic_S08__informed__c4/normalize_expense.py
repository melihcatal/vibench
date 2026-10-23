from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Description of the line item")
    amount: Optional[float] = Field(None, description="Amount for the line item")
    quantity: Optional[float] = Field(None, description="Quantity of the line item")


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor or merchant name")
    date: Optional[str] = Field(None, description="Date of the expense in ISO format")
    total: Optional[float] = Field(None, description="Total amount of the expense")
    tax: Optional[float] = Field(None, description="Tax amount")
    currency: Optional[str] = Field("USD", description="Currency of the expense")
    line_items: list[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


def normalize_expense(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    normalized = NormalizedExpense()

    if "vendor" in extracted_data:
        normalized.vendor = extracted_data["vendor"]
    elif "merchant" in extracted_data:
        normalized.vendor = extracted_data["merchant"]

    if "date" in extracted_data:
        normalized.date = extracted_data["date"]

    if "total" in extracted_data:
        normalized.total = extracted_data["total"]

    if "tax" in extracted_data:
        normalized.tax = extracted_data["tax"]

    if "confidence" in extracted_data:
        normalized.confidence = extracted_data["confidence"]

    if "line_items" in extracted_data:
        normalized.line_items = [
            LineItem(
                description=item.get("description"),
                amount=item.get("amount"),
                quantity=item.get("quantity"),
            )
            for item in extracted_data["line_items"]
        ]
    elif "items" in extracted_data:
        normalized.line_items = [
            LineItem(
                description=item.get("description"),
                amount=item.get("total_price"),
                quantity=item.get("quantity"),
            )
            for item in extracted_data["items"]
        ]

    return normalized.model_dump(exclude_none=True)
