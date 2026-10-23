from typing import Dict, Any, List, Optional, TypedDict
from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: Optional[str] = Field(
        default=None, description="Description of the line item"
    )
    quantity: Optional[float] = Field(default=None, description="Quantity of the item")
    unit_price: Optional[float] = Field(
        default=None, description="Unit price of the item"
    )
    amount: Optional[float] = Field(
        default=None, description="Total amount for the line item"
    )


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(default=None, description="Vendor or merchant name")
    date: Optional[str] = Field(default=None, description="Date of the transaction")
    total: Optional[float] = Field(default=None, description="Total amount")
    tax: Optional[float] = Field(default=None, description="Tax amount")
    items: List[LineItem] = Field(
        default_factory=list, description="List of line items or items"
    )
    currency: Optional[str] = Field(
        default=None, description="Currency of the transaction"
    )
    document_type: Optional[str] = Field(
        default=None, description="Type of document (e.g., invoice, receipt)"
    )


class DocumentField(TypedDict):
    field_name: str
    value: Any
    confidence: float


def normalize_document_fields(
    fields: Dict[str, DocumentField], document_type: str
) -> NormalizedExpense:
    """Normalize extracted document fields into a standard schema."""
    normalized = NormalizedExpense(document_type=document_type)

    for field_name, field_data in fields.items():
        value = field_data.get("value")
        if not value:
            continue

        if field_name == "vendor":
            normalized.vendor = value
        elif field_name == "merchant":
            normalized.vendor = value
        elif field_name == "date":
            normalized.date = value
        elif field_name == "total":
            normalized.total = float(value)
        elif field_name == "tax":
            normalized.tax = float(value)
        elif field_name == "line_items" or field_name == "items":
            for item in value:
                line_item = LineItem(
                    description=item.get("description"),
                    quantity=float(item.get("quantity", 0)),
                    unit_price=float(item.get("unit_price", 0)),
                    amount=float(item.get("amount", 0)),
                )
                normalized.items.append(line_item)
        elif field_name == "currency":
            normalized.currency = value

    return normalized
