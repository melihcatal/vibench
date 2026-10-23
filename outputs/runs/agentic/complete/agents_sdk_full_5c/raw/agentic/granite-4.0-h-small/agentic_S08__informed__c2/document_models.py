from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import List, Optional


class Item(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: float = Field(..., gt=0, description="Quantity")
    unit_price: float = Field(..., gt=0, description="Unit price")
    total: Optional[float] = Field(None, description="Line total")


class Expense(BaseModel):
    vendor: Optional[str] = Field(None, description="Vendor name")
    date: Optional[datetime] = Field(None, description="Invoice / receipt date")
    total: Optional[float] = Field(None, description="Total amount")
    currency: Optional[str] = Field(None, default="USD", description="Currency code")
    items: List[Item] = Field(default_factory=list, description="List of line items")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")

    @validator("total", pre=True, always=True)
    def validate_total(cls, v, values):
        if v is None and "line_items" in values:
            # Sum line items if total not provided
            v = sum(item.total or 0 for item in values["items"])
        return v
