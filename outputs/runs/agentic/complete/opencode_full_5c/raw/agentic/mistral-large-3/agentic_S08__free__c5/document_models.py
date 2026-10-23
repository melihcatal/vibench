from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentEntity(BaseModel):
    type_: str = Field(..., alias="type")
    mention_text: str
    normalized_value: Optional[Dict[str, Any]] = None
    confidence: Optional[float] = None
    properties: Optional[List["DocumentEntity"]] = None


class DocumentResponse(BaseModel):
    text: str
    entities: List[DocumentEntity]
    confidence: float
    mime_type: str


class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Description of the line item")
    quantity: Optional[float] = Field(None, description="Quantity of the item")
    amount: Optional[float] = Field(None, description="Amount for the line item")
    price: Optional[float] = Field(None, description="Price per unit")


class ExtractedInvoice(BaseModel):
    vendor: Optional[str] = Field(None, description="Name of the vendor")
    date: Optional[str] = Field(
        None, description="Date of the invoice in ISO 8601 format"
    )
    total: Optional[float] = Field(None, description="Total amount of the invoice")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


class ExtractedReceipt(BaseModel):
    merchant: Optional[str] = Field(None, description="Name of the merchant")
    tax: Optional[float] = Field(None, description="Tax amount")
    total: Optional[float] = Field(None, description="Total amount of the receipt")
    items: List[LineItem] = Field(default_factory=list, description="List of items")
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(None, description="Name of the vendor or merchant")
    date: Optional[str] = Field(
        None, description="Date of the expense in ISO 8601 format"
    )
    total: Optional[float] = Field(None, description="Total amount of the expense")
    tax: Optional[float] = Field(None, description="Tax amount")
    currency: Optional[str] = Field("USD", description="Currency of the expense")
    line_items: List[LineItem] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


# Update forward references for DocumentEntity
DocumentEntity.update_forward_refs()
