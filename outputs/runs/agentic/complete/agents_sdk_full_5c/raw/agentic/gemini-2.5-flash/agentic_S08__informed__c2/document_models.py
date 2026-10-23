from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: str = Field(..., description="Description of the line item")
    amount: float = Field(..., description="Amount of the line item")
    currency: Optional[str] = Field(None, description="Currency of the line item amount")

class InvoiceExtractionResult(BaseModel):
    vendor: str = Field(..., description="Name of the invoice vendor")
    date: str = Field(..., description="Date of the invoice")
    total: float = Field(..., description="Total amount of the invoice")
    line_items: List[LineItem] = Field(default_factory=list, description="List of line items on the invoice")
    currency: Optional[str] = Field(None, description="Currency of the invoice total")
    confidence: Optional[float] = Field(None, description="Confidence score for the extraction")

class ReceiptExtractionResult(BaseModel):
    merchant: str = Field(..., description="Name of the receipt merchant")
    tax: float = Field(..., description="Tax amount on the receipt")
    total: float = Field(..., description="Total amount of the receipt")
    items: List[LineItem] = Field(default_factory=list, description="List of items on the receipt")
    currency: Optional[str] = Field(None, description="Currency of the receipt total")
    confidence: Optional[float] = Field(None, description="Confidence score for the extraction")

class NormalizedExpense(BaseModel):
    vendor: str = Field(..., description="Standardized vendor name")
    date: str = Field(..., description="Standardized expense date (ISO format)")
    amount: float = Field(..., description="Standardized total amount")
    currency: str = Field(..., description="Standardized currency (ISO 4217 code)")
    description: str = Field(..., description="Overall description of the expense")
    line_items: List[LineItem] = Field(default_factory=list, description="Standardized list of line items")
    original_document_type: Optional[str] = Field(None, description="Original document type (e.g., invoice, receipt)")
    extracted_confidence: Optional[float] = Field(None, description="Overall confidence score from extraction")

if __name__ == '__main__':
    # Example instantiation
    invoice_res = InvoiceExtractionResult(
        vendor="Acme Corp",
        date="2023-10-26",
        total=123.45,
        line_items=[LineItem(description="Item X", amount=100.0)],
        currency="USD"
    )
    print(invoice_res.model_dump_json(indent=2))
