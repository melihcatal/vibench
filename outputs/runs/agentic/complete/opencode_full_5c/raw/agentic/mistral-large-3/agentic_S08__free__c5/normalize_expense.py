from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime
import re


class LineItem(BaseModel):
    description: Optional[str] = Field(None, description="Description of the line item")
    quantity: Optional[float] = Field(None, description="Quantity of the item")
    amount: Optional[float] = Field(None, description="Amount for the line item")


class NormalizedExpense(BaseModel):
    vendor: Optional[str] = Field(None, description="Name of the vendor or merchant")
    date: Optional[str] = Field(
        None, description="Date of the expense in ISO 8601 format"
    )
    total: Optional[float] = Field(None, description="Total amount of the expense")
    tax: Optional[float] = Field(None, description="Tax amount")
    currency: Optional[str] = Field("USD", description="Currency of the expense")
    line_items: Optional[list[LineItem]] = Field(
        default_factory=list, description="List of line items"
    )
    confidence: Optional[float] = Field(
        None, description="Confidence score of the extraction"
    )


def normalize_expense(extracted_data: Dict[str, Any]) -> NormalizedExpense:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    normalized = NormalizedExpense()

    if "vendor" in extracted_data:
        normalized.vendor = _clean_text(extracted_data["vendor"])
    elif "merchant" in extracted_data:
        normalized.vendor = _clean_text(extracted_data["merchant"])

    if "date" in extracted_data:
        normalized.date = _normalize_date(extracted_data["date"])

    if "total" in extracted_data:
        normalized.total = float(extracted_data["total"])

    if "tax" in extracted_data:
        normalized.tax = float(extracted_data["tax"])

    if "confidence" in extracted_data:
        normalized.confidence = float(extracted_data["confidence"])

    if "line_items" in extracted_data:
        normalized.line_items = [
            LineItem(
                description=_clean_text(item.get("description")),
                quantity=float(item["quantity"]) if item.get("quantity") else None,
                amount=float(item["amount"]) if item.get("amount") else None,
            )
            for item in extracted_data["line_items"]
            if any([item.get("description"), item.get("quantity"), item.get("amount")])
        ]
    elif "items" in extracted_data:
        normalized.line_items = [
            LineItem(
                description=_clean_text(item.get("description")),
                quantity=float(item["quantity"]) if item.get("quantity") else None,
                amount=float(item["price"]) if item.get("price") else None,
            )
            for item in extracted_data["items"]
            if any([item.get("description"), item.get("quantity"), item.get("price")])
        ]

    return normalized


def _clean_text(text: Optional[str]) -> Optional[str]:
    if not text:
        return None
    return re.sub(r"\s+", " ", text).strip()


def _normalize_date(date_str: Optional[str]) -> Optional[str]:
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str).isoformat()
    except (ValueError, TypeError):
        return date_str
