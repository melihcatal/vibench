from typing import Dict, Any, TypedDict, List
from datetime import datetime
import pytz


class NormalizedLineItem(TypedDict):
    description: str
    quantity: float
    unit_price: float
    amount: float
    category: str


class NormalizedExpense(TypedDict):
    vendor: str
    merchant: str
    date: str
    total: float
    tax: float
    currency: str
    line_items: List[NormalizedLineItem]
    items: List[Dict[str, Any]]
    document_type: str
    confidence: float


def normalize_expense(
    invoice_fields: Dict[str, Any] = None,
    receipt_fields: Dict[str, Any] = None,
) -> NormalizedExpense:
    if invoice_fields and receipt_fields:
        raise ValueError(
            "Only one of invoice_fields or receipt_fields should be provided"
        )

    if invoice_fields:
        return _normalize_invoice(invoice_fields)
    elif receipt_fields:
        return _normalize_receipt(receipt_fields)
    else:
        raise ValueError("Either invoice_fields or receipt_fields must be provided")


def _normalize_invoice(invoice_fields: Dict[str, Any]) -> NormalizedExpense:
    date = invoice_fields.get("date", "")
    try:
        parsed_date = datetime.strptime(date, "%Y-%m-%d")
        date = parsed_date.astimezone(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    except (ValueError, TypeError):
        date = ""

    line_items = []
    for item in invoice_fields.get("line_items", []):
        line_items.append(
            {
                "description": item.get("description", ""),
                "quantity": float(item.get("quantity", 0.0)),
                "unit_price": float(item.get("unit_price", 0.0)),
                "amount": float(item.get("amount", 0.0)),
                "category": _categorize_item(item.get("description", "")),
            }
        )

    return {
        "vendor": invoice_fields.get("vendor", ""),
        "merchant": "",
        "date": date,
        "total": float(invoice_fields.get("total", 0.0)),
        "tax": 0.0,
        "currency": "USD",
        "line_items": line_items,
        "items": [],
        "document_type": "invoice",
        "confidence": float(invoice_fields.get("confidence", 0.0)),
    }


def _normalize_receipt(receipt_fields: Dict[str, Any]) -> NormalizedExpense:
    date = datetime.now(pytz.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    items = []
    for item in receipt_fields.get("items", []):
        items.append(
            {
                "name": item.get("name", ""),
                "price": float(item.get("price", 0.0)),
                "quantity": float(item.get("quantity", 1.0))
                if item.get("quantity") is not None
                else 1.0,
            }
        )

    return {
        "vendor": "",
        "merchant": receipt_fields.get("merchant", ""),
        "date": date,
        "total": float(receipt_fields.get("total", 0.0)),
        "tax": float(receipt_fields.get("tax", 0.0)),
        "currency": "USD",
        "line_items": [],
        "items": items,
        "document_type": "receipt",
        "confidence": float(receipt_fields.get("confidence", 0.0)),
    }


def _categorize_item(description: str) -> str:
    description = description.lower()
    if any(
        keyword in description
        for keyword in ["software", "saas", "license", "subscription"]
    ):
        return "software"
    elif any(keyword in description for keyword in ["hardware", "device", "equipment"]):
        return "hardware"
    elif any(
        keyword in description for keyword in ["travel", "flight", "hotel", "taxi"]
    ):
        return "travel"
    elif any(
        keyword in description for keyword in ["meal", "food", "restaurant", "lunch"]
    ):
        return "meals"
    else:
        return "miscellaneous"
