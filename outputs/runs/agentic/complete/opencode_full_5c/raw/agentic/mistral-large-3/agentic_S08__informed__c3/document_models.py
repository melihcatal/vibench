from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(
        default=None, description="Line item description"
    )
    quantity: Optional[float] = Field(default=None, description="Line item quantity")
    unit_price: Optional[float] = Field(
        default=None, description="Line item unit price"
    )
    amount: Optional[float] = Field(default=None, description="Line item total amount")


class InvoiceFields(BaseModel):
    vendor_name: Optional[str] = Field(default=None, description="Vendor name")
    vendor_address: Optional[str] = Field(default=None, description="Vendor address")
    invoice_date: Optional[str] = Field(
        default=None, description="Invoice date in YYYY-MM-DD"
    )
    invoice_number: Optional[str] = Field(default=None, description="Invoice number")
    total_amount: Optional[float] = Field(
        default=None, description="Total invoice amount"
    )
    tax_amount: Optional[float] = Field(default=None, description="Tax amount")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(default=None, description="Confidence score")


class ReceiptFields(BaseModel):
    merchant_name: Optional[str] = Field(default=None, description="Merchant name")
    merchant_address: Optional[str] = Field(
        default=None, description="Merchant address"
    )
    transaction_date: Optional[str] = Field(
        default=None, description="Transaction date in YYYY-MM-DD"
    )
    total_amount: Optional[float] = Field(default=None, description="Total amount")
    tax_amount: Optional[float] = Field(default=None, description="Tax amount")
    items: List[Dict[str, Any]] = Field(
        default_factory=list, description="List of purchased items"
    )
    confidence: Optional[float] = Field(default=None, description="Confidence score")


class NormalizedExpense(BaseModel):
    expense_type: str = Field(
        ..., description="Type of expense: 'invoice' or 'receipt'"
    )
    vendor_merchant_name: str = Field(..., description="Vendor or merchant name")
    date: str = Field(..., description="Date in YYYY-MM-DD")
    total_amount: float = Field(..., description="Total amount")
    tax_amount: Optional[float] = Field(default=None, description="Tax amount")
    currency: str = Field(default="USD", description="Currency code")
    line_items: List[Dict[str, Any]] = Field(
        default_factory=list, description="Line items or items"
    )
    document_reference: Optional[str] = Field(
        default=None, description="Document reference or ID"
    )
    confidence: float = Field(..., description="Overall confidence score")


def parse_textract_expense_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parses AWS Textract AnalyzeExpense response into structured fields.
    """
    expense_documents = response.get("ExpenseDocuments", [])
    if not expense_documents:
        return {}

    fields = expense_documents[0].get("SummaryFields", {})
    line_items = []

    for item in expense_documents[0].get("LineItemGroups", []):
        for line_item in item.get("LineItems", []):
            line_data = {}
            for field in line_item.get("LineItemExpenseFields", []):
                field_type = field.get("Type", {}).get("Text", "").lower()
                value = field.get("ValueDetection", {}).get("Text", "")
                if field_type == "description":
                    line_data["description"] = value
                elif field_type == "quantity":
                    line_data["quantity"] = float(value) if value else None
                elif field_type == "unitprice":
                    line_data["unit_price"] = float(value) if value else None
                elif field_type == "amount":
                    line_data["amount"] = float(value) if value else None
            if line_data:
                line_items.append(line_data)

    result = {}
    for field in fields:
        field_type = field.get("Type", {}).get("Text", "").lower()
        value = field.get("ValueDetection", {}).get("Text", "")
        if field_type == "vendorname":
            result["vendor_name"] = value
        elif field_type == "vendoraddress":
            result["vendor_address"] = value
        elif field_type == "invoicedate":
            result["invoice_date"] = value
        elif field_type == "invoicereceiptdate":
            result["invoice_date"] = value
        elif field_type == "invoicenumber":
            result["invoice_number"] = value
        elif field_type == "total":
            result["total_amount"] = float(value) if value else None
        elif field_type == "tax":
            result["tax_amount"] = float(value) if value else None

    result["line_items"] = line_items
    result["confidence"] = (
        sum(field.get("ValueDetection", {}).get("Confidence", 0) for field in fields)
        / len(fields)
        if fields
        else 0
    )

    return result
