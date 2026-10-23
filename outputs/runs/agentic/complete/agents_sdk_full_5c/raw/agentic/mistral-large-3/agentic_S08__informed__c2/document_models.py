from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class LineItemSchema(BaseModel):
    description: Optional[str] = Field(default=None, description="Description of the line item")
    quantity: Optional[float] = Field(default=None, description="Quantity of the item")
    unit_price: Optional[float] = Field(default=None, description="Unit price of the item")
    amount: Optional[float] = Field(default=None, description="Total amount for the line item")

class ExpenseSchema(BaseModel):
    source_type: str = Field(..., description="Type of source document (invoice or receipt)")
    vendor: Optional[str] = Field(default=None, description="Vendor or merchant name")
    date: Optional[str] = Field(default=None, description="Date of the transaction in ISO format")
    total_amount: Optional[float] = Field(default=None, description="Total amount of the transaction")
    tax_amount: Optional[float] = Field(default=None, description="Tax amount for the transaction")
    line_items: List[LineItemSchema] = Field(default_factory=list, description="List of line items")
    currency: str = Field(default="USD", description="Currency of the transaction")
    confidence: float = Field(default=0.0, description="Confidence score of the extraction")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Original extracted fields and metadata")

class InvoiceSchema(ExpenseSchema):
    invoice_number: Optional[str] = Field(default=None, description="Invoice number")
    due_date: Optional[str] = Field(default=None, description="Due date of the invoice in ISO format")

class ReceiptSchema(ExpenseSchema):
    payment_method: Optional[str] = Field(default=None, description="Payment method used")
    transaction_id: Optional[str] = Field(default=None, description="Transaction ID or reference")