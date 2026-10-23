from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Description of the line item")
    amount: Optional[float] = Field(None, description="Amount for the line item")
    quantity: Optional[float] = Field(None, description="Quantity of the line item")


class ExtractedInvoice(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor name")
    date: Optional[str] = Field(None, description="Invoice date in ISO format")
    total: Optional[float] = Field(None, description="Total invoice amount")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


class ExtractedReceipt(BaseModel):
    merchant: Optional[str] = Field(None, description="Merchant name")
    tax: Optional[float] = Field(None, description="Tax amount")
    total: Optional[float] = Field(None, description="Total amount")
    items: List[LineItem] = Field(default_factory=list, description="List of items")
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor or merchant name")
    date: Optional[str] = Field(None, description="Date of the expense in ISO format")
    total: Optional[float] = Field(None, description="Total amount of the expense")
    tax: Optional[float] = Field(None, description="Tax amount")
    currency: Optional[str] = Field("USD", description="Currency of the expense")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


def parse_azure_invoice_result(result: Dict[str, Any]) -> ExtractedInvoice:
    """Parses Azure Document Intelligence invoice result into a structured model."""
    invoice = ExtractedInvoice()

    if result.get("documents"):
        fields = result["documents"][0].fields

        if fields.get("VendorName"):
            invoice.vendor = fields["VendorName"].value

        if fields.get("InvoiceDate"):
            invoice.date = fields["InvoiceDate"].value.isoformat()

        if fields.get("InvoiceTotal"):
            invoice.total = float(fields["InvoiceTotal"].value)

        if fields.get("Items"):
            for item in fields["Items"].value:
                line_item = LineItem(
                    description=item.value.get("Description", {}).value
                    if item.value.get("Description")
                    else None,
                    amount=float(item.value["Amount"].value)
                    if item.value.get("Amount")
                    else None,
                    quantity=float(item.value["Quantity"].value)
                    if item.value.get("Quantity")
                    else None,
                )
                invoice.line_items.append(line_item)

    invoice.confidence = result.get("confidence", 0.0)
    return invoice


def parse_mindee_receipt_result(result: Dict[str, Any]) -> ExtractedReceipt:
    """Parses Mindee receipt result into a structured model."""
    receipt = ExtractedReceipt()

    if result.get("document"):
        prediction = result["document"].inference.prediction

        if prediction.merchant_name:
            receipt.merchant = prediction.merchant_name.value

        if prediction.total_tax:
            receipt.tax = float(prediction.total_tax.value)

        if prediction.total_amount:
            receipt.total = float(prediction.total_amount.value)

        if prediction.line_items:
            for item in prediction.line_items:
                receipt.items.append(
                    LineItem(
                        description=item.description,
                        quantity=item.quantity,
                        amount=float(item.total_amount),
                    )
                )

    receipt.confidence = result.get("confidence", 0.0)
    return receipt
