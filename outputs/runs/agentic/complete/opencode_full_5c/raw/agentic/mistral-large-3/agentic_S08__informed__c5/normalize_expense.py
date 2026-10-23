from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(
        default=None, description="Description of the line item"
    )
    amount: Optional[float] = Field(default=None, description="Amount of the line item")
    quantity: Optional[float] = Field(
        default=None, description="Quantity of the line item"
    )


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(default=None, description="Vendor or merchant name")
    date: Optional[str] = Field(
        default=None, description="Date of the expense in YYYY-MM-DD format"
    )
    total: Optional[float] = Field(
        default=None, description="Total amount of the expense"
    )
    tax: Optional[float] = Field(default=None, description="Tax amount of the expense")
    items: list[LineItem] = Field(
        default_factory=list, description="List of line items or items"
    )
    document_type: str = Field(..., description="Type of document (invoice or receipt)")
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of the extraction"
    )


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> NormalizedExpense:
    if document_type == "invoice":
        return _normalize_invoice(extracted_data)
    elif document_type == "receipt":
        return _normalize_receipt(extracted_data)
    else:
        raise ValueError(f"Unsupported document type: {document_type}")


def _normalize_invoice(invoice_data: Dict[str, Any]) -> NormalizedExpense:
    return NormalizedExpense(
        vendor=invoice_data.get("vendor"),
        date=invoice_data.get("date"),
        total=invoice_data.get("total"),
        tax=None,  # Tax is not always available in invoice data
        items=[
            LineItem(
                description=item.get("description"),
                amount=item.get("amount"),
                quantity=item.get("quantity"),
            )
            for item in invoice_data.get("line_items", [])
        ],
        document_type="invoice",
        confidence=invoice_data.get("confidence"),
    )


def _normalize_receipt(receipt_data: Dict[str, Any]) -> NormalizedExpense:
    return NormalizedExpense(
        vendor=receipt_data.get("merchant"),
        date=None,  # Date is not always available in receipt data
        total=receipt_data.get("total"),
        tax=receipt_data.get("tax"),
        items=[
            LineItem(
                description=item.get("description"),
                amount=item.get("amount"),
                quantity=None,  # Quantity is not always available in receipt data
            )
            for item in receipt_data.get("items", [])
        ],
        document_type="receipt",
        confidence=receipt_data.get("confidence"),
    )
