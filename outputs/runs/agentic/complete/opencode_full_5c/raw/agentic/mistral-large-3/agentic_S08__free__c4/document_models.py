from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(
        default=None, description="Description of the line item"
    )
    quantity: Optional[float] = Field(default=None, description="Quantity of the item")
    unit_price: Optional[float] = Field(
        default=None, description="Unit price of the item"
    )
    amount: Optional[float] = Field(
        default=None, description="Total amount for the line item"
    )


class InvoiceFields(BaseModel):
    vendor: Optional[str] = Field(default=None, description="Vendor name")
    date: Optional[str] = Field(default=None, description="Invoice date")
    total: Optional[float] = Field(default=None, description="Total invoice amount")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of extraction"
    )


class ReceiptFields(BaseModel):
    merchant: Optional[str] = Field(default=None, description="Merchant name")
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
        default=None, description="Unique expense identifier"
    )
    vendor: Optional[str] = Field(default=None, description="Vendor or merchant name")
    date: Optional[str] = Field(default=None, description="Expense date")
    amount: Optional[float] = Field(default=None, description="Total expense amount")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    currency: Optional[str] = Field(
        default="USD", description="Currency of the expense"
    )
    category: Optional[str] = Field(default=None, description="Expense category")
    line_items: List[Dict[str, Any]] = Field(
        default_factory=list, description="Detailed line items"
    )
    confidence: Optional[float] = Field(
        default=None, description="Overall confidence score"
    )


def normalize_invoice_fields(invoice: InvoiceFields) -> NormalizedExpense:
    line_items = [
        {
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "amount": item.amount,
        }
        for item in invoice.line_items
    ]

    return NormalizedExpense(
        vendor=invoice.vendor,
        date=invoice.date,
        amount=invoice.total,
        line_items=line_items,
        confidence=invoice.confidence,
    )


def normalize_receipt_fields(receipt: ReceiptFields) -> NormalizedExpense:
    return NormalizedExpense(
        vendor=receipt.merchant,
        date=None,  # Receipts may not always have a date in the same format
        amount=receipt.total,
        tax=receipt.tax,
        line_items=receipt.items,
        confidence=receipt.confidence,
    )
