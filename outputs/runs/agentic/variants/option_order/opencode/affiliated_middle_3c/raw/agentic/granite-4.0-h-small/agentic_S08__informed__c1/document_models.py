from typing import List, Dict

InvoiceItem = Dict[str, Any]
ReceiptItem = Dict[str, Any]

InvoiceSchema = Dict[str, Any]
ReceiptSchema = Dict[str, Any]

ExpenseSchema = Dict[str, Any]

# Simple helpers to declare typed model structures for local usage


def create_invoice_model() -> InvoiceSchema:
    return {"vendor": "", "date": "", "total": 0.0, "line_items": []}


def create_receipt_model() -> ReceiptSchema:
    return {"merchant": "", "date": "", "total": 0.0, "items": []}


# Export the helper defined earlier for normalising raw OCR responses
def normalize_expense(raw_data: dict) -> ExpenseSchema:
    """Normalize extracted expense fields into a common JSON schema.

    Expected keys:
      - vendor / merchant
      - date
      - total
      - items / line_items
    """
    normalized = {
        "vendor": raw_data.get("vendor") or raw_data.get("merchant"),
        "date": raw_data.get("date"),
        "total": float(raw_data.get("total", 0)),
        "items": [],
    }
    items = raw_data.get("line_items") or raw_data.get("items")
    if items:
        for item in items:
            normalized["items"].append(
                {
                    "description": item.get("description") or item.get("name"),
                    "quantity": item.get("quantity", 1),
                    "unit_price": float(item.get("unit_price", 0)),
                    "total": float(item.get("total", 0)),
                }
            )
    return normalized
