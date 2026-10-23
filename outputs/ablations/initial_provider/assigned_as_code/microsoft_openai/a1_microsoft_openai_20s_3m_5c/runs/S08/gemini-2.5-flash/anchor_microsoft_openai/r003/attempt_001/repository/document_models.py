from pydantic import BaseModel, Field
from typing import List, Optional


class ExtractedLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[str] = None
    amount: Optional[str] = None


class ExtractedInvoice(BaseModel):
    vendor: Optional[str] = None
    date: Optional[str] = None
    total: Optional[str] = None
    line_items: List[ExtractedLineItem] = Field(default_factory=list)


class ExtractedReceipt(BaseModel):
    merchant: Optional[str] = None
    tax: Optional[str] = None
    total: Optional[str] = None
    items: List[ExtractedLineItem] = Field(default_factory=list)


class NormalizedExpense(BaseModel):
    transaction_id: str = Field(..., description="Unique transaction identifier")
    document_type: str = Field(..., description="Type of document (e.g., invoice, receipt)")
    vendor_merchant_name: str = Field(..., description="Name of the vendor or merchant")
    transaction_date: str = Field(..., description="Date of the transaction in YYYY-MM-DD format")
    total_amount: float = Field(..., description="Total amount of the transaction")
    currency: str = Field(..., description="Currency of the transaction (e.g., USD, EUR)")
    tax_amount: Optional[float] = None
    line_items: List[dict] = Field(default_factory=list)
    extracted_raw_data: Optional[dict] = None
    validation_errors: List[str] = Field(default_factory=list)
    confidence_score: float = Field(default=0.0)

