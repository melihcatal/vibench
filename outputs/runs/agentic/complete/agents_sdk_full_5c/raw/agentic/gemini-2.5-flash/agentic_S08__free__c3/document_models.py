
from pydantic import BaseModel, Field
from typing import List, Optional

class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Description of the line item.")
    amount: Optional[float] = Field(None, description="Monetary amount of the line item.")
    quantity: Optional[int] = Field(1, description="Quantity of the line item.")

class ExpenseRecord(BaseModel):
    document_type: str = Field(..., description="Type of the document (e.g., 'invoice', 'receipt').")
    vendor_name: Optional[str] = Field(None, description="Name of the vendor or merchant.")
    transaction_date: Optional[str] = Field(None, description="Date of the transaction (YYYY-MM-DD format).")
    total_amount: Optional[float] = Field(None, description="Total amount of the expense.")
    tax_amount: Optional[float] = Field(None, description="Total tax amount, if available.")
    currency: Optional[str] = Field("USD", description="Currency of the transaction.")
    line_items: List[LineItem] = Field([], description="List of individual line items.")
    notes: Optional[str] = Field(None, description="Any additional notes or memo text from the document.")
    document_id: Optional[str] = Field(None, description="Unique identifier for the original document.")
    validation_status: Optional[str] = Field("pending", description="Status of validation (e.g., 'pending', 'valid', 'invalid').")
    summary: Optional[str] = Field(None, description="Generated summary of the expense.")
    safety_attributes: Optional[dict] = Field(None, description="Safety moderation attributes.")
    translated_notes: Optional[str] = Field(None, description="Translated version of the notes.")
