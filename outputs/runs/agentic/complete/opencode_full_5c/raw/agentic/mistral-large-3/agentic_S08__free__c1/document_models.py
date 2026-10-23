from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(
        default=None, description="Description of the line item"
    )
    quantity: Optional[float] = Field(default=None, description="Quantity of the item")
    unit_price: Optional[float] = Field(default=None, description="Price per unit")
    amount: Optional[float] = Field(
        default=None, description="Total amount for the line item"
    )


class InvoiceFields(BaseModel):
    vendor: Optional[str] = Field(default=None, description="Name of the vendor")
    date: Optional[str] = Field(
        default=None, description="Invoice date in YYYY-MM-DD format"
    )
    total: Optional[float] = Field(default=None, description="Total invoice amount")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of extraction"
    )


class ReceiptFields(BaseModel):
    merchant: Optional[str] = Field(default=None, description="Name of the merchant")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    total: Optional[float] = Field(default=None, description="Total receipt amount")
    items: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of purchased items"
    )
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of extraction"
    )


class NormalizedExpense(BaseModel):
    expense_id: Optional[str] = Field(
        default=None, description="Unique identifier for the expense"
    )
    vendor_merchant: Optional[str] = Field(
        default=None, description="Vendor or merchant name"
    )
    date: Optional[str] = Field(
        default=None, description="Date of the expense in YYYY-MM-DD format"
    )
    amount: Optional[float] = Field(default=None, description="Total amount")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    currency: Optional[str] = Field(
        default="USD", description="Currency of the expense"
    )
    category: Optional[str] = Field(default=None, description="Expense category")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


def parse_date(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    return date_str.split("T")[0]


def normalize_currency(amount: Optional[float]) -> Optional[float]:
    if amount is None:
        return None
    return round(amount, 2)
