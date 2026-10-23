from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class DocumentField(BaseModel):
    value: Optional[Any] = Field(
        default=None, description="Extracted value of the field"
    )
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of the extraction"
    )


class LineItem(DocumentField):
    description: Optional[str] = Field(
        default=None, description="Description of the line item"
    )
    amount: Optional[float] = Field(default=None, description="Amount of the line item")
    quantity: Optional[float] = Field(
        default=None, description="Quantity of the line item"
    )


class InvoiceData(BaseModel):
    vendor: Optional[DocumentField] = Field(default=None, description="Vendor name")
    date: Optional[DocumentField] = Field(default=None, description="Invoice date")
    total: Optional[DocumentField] = Field(default=None, description="Invoice total")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        default=None, description="Overall confidence score"
    )


class ReceiptData(BaseModel):
    merchant: Optional[DocumentField] = Field(default=None, description="Merchant name")
    tax: Optional[DocumentField] = Field(default=None, description="Tax amount")
    total: Optional[DocumentField] = Field(default=None, description="Total amount")
    items: List[LineItem] = Field(default_factory=list, description="List of items")
    confidence: Optional[float] = Field(
        default=None, description="Overall confidence score"
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
    items: List[LineItem] = Field(
        default_factory=list, description="List of line items or items"
    )
    document_type: str = Field(..., description="Type of document (invoice or receipt)")
    confidence: Optional[float] = Field(
        default=None, description="Confidence score of the extraction"
    )


def parse_azure_invoice_result(result: Dict[str, Any]) -> InvoiceData:
    invoice_data = InvoiceData()
    if result.documents and len(result.documents) > 0:
        document = result.documents[0]
        invoice_data.vendor = DocumentField(
            value=document.fields.get("VendorName", {}).value
            if document.fields.get("VendorName")
            else None,
            confidence=document.fields.get("VendorName", {}).confidence
            if document.fields.get("VendorName")
            else None,
        )
        invoice_data.date = DocumentField(
            value=document.fields.get("InvoiceDate", {}).value.strftime("%Y-%m-%d")
            if document.fields.get("InvoiceDate")
            and document.fields.get("InvoiceDate", {}).value
            else None,
            confidence=document.fields.get("InvoiceDate", {}).confidence
            if document.fields.get("InvoiceDate")
            else None,
        )
        invoice_data.total = DocumentField(
            value=float(document.fields.get("InvoiceTotal", {}).value)
            if document.fields.get("InvoiceTotal")
            and document.fields.get("InvoiceTotal", {}).value
            else None,
            confidence=document.fields.get("InvoiceTotal", {}).confidence
            if document.fields.get("InvoiceTotal")
            else None,
        )
        if document.fields.get("Items"):
            for item in document.fields.get("Items", {}).value:
                line_item = LineItem(
                    description=item.value.get("Description", {}).value
                    if item.value.get("Description")
                    else None,
                    amount=float(item.value.get("Amount", {}).value)
                    if item.value.get("Amount") and item.value.get("Amount", {}).value
                    else None,
                    quantity=float(item.value.get("Quantity", {}).value)
                    if item.value.get("Quantity")
                    and item.value.get("Quantity", {}).value
                    else None,
                )
                invoice_data.line_items.append(line_item)
        invoice_data.confidence = result.confidence
    return invoice_data


def parse_mindee_receipt_result(result: Dict[str, Any]) -> ReceiptData:
    receipt_data = ReceiptData()
    prediction = result.document.inference.prediction
    receipt_data.merchant = DocumentField(
        value=prediction.merchant_name.value,
        confidence=prediction.merchant_name.confidence,
    )
    if prediction.taxes and len(prediction.taxes) > 0:
        receipt_data.tax = DocumentField(
            value=float(prediction.taxes[0].value),
            confidence=prediction.taxes[0].confidence,
        )
    receipt_data.total = DocumentField(
        value=float(prediction.total_amount.value)
        if prediction.total_amount.value
        else None,
        confidence=prediction.total_amount.confidence,
    )
    for item in prediction.line_items:
        line_item = LineItem(
            description=item.description.value if item.description else None,
            amount=float(item.total_amount.value) if item.total_amount else None,
        )
        receipt_data.items.append(line_item)
    receipt_data.confidence = prediction.confidence
    return receipt_data
