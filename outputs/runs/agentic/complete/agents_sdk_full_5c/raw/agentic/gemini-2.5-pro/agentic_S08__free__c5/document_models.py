# document_models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ExtractedLineItem(BaseModel):
    description: Optional[str] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

class ExtractedInvoice(BaseModel):
    vendor_name: Optional[str] = None
    invoice_date: Optional[str] = None
    total_amount: Optional[float] = None
    line_items: List[ExtractedLineItem] = []
    raw_fields: Dict[str, Any] = {}

class ExtractedReceipt(BaseModel):
    merchant_name: Optional[str] = None
    transaction_date: Optional[str] = None
    total_amount: Optional[float] = None
    tax_amount: Optional[float] = None
    line_items: List[ExtractedLineItem] = []
    raw_fields: Dict[str, Any] = {}

class NormalizedLineItem(BaseModel):
    item_description: str = Field(description="Description of the item or service.")
    item_quantity: float = Field(description="Quantity of the item.")
    item_unit_price: float = Field(description="Price per unit of the item.")
    item_total: float = Field(description="Total price for the line item.")

class NormalizedExpense(BaseModel):
    vendor: str = Field(description="Vendor or merchant name.")
    transaction_date: str = Field(description="Date of the transaction in YYYY-MM-DD format.")
    total: float = Field(description="Total amount of the expense.")
    currency: str = Field(default="USD", description="Currency of the transaction (ISO 4217 code).")
    category: str = Field(default="Uncategorized", description="Expense category.")
    line_items: List[NormalizedLineItem] = Field(description="List of individual items purchased.")
    source_document_type: str = Field(description="Type of the source document (e.g., 'invoice', 'receipt').")
