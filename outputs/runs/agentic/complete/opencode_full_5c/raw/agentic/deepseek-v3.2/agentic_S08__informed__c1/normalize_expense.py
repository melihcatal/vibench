import json
from typing import Dict, Any, List
from datetime import datetime
from document_models import ExpenseRecord, LineItem


def normalize_expense(
    extracted_data: Dict[str, Any], source_type: str = "invoice"
) -> Dict[str, Any]:
    """
    Normalize extracted expense fields into a standard JSON schema.
    """
    normalized = {
        "expense_id": f"exp_{int(datetime.now().timestamp())}",
        "source_type": source_type,
        "extraction_timestamp": datetime.now().isoformat(),
        "vendor": None,
        "merchant": None,
        "date": None,
        "total_amount": 0.0,
        "tax_amount": 0.0,
        "currency": "USD",
        "line_items": [],
        "metadata": {},
    }

    if source_type == "invoice":
        normalized["vendor"] = extracted_data.get("vendor")
        normalized["date"] = extracted_data.get("date")
        normalized["total_amount"] = extracted_data.get("total", 0.0)

        line_items = extracted_data.get("line_items", [])
        for item in line_items:
            line_item = {
                "description": item.get("description", ""),
                "quantity": item.get("quantity", 1.0),
                "unit_price": item.get("amount", 0.0)
                / max(item.get("quantity", 1.0), 1.0),
                "total": item.get("amount", 0.0),
            }
            normalized["line_items"].append(line_item)

    elif source_type == "receipt":
        normalized["merchant"] = extracted_data.get("merchant")
        normalized["date"] = datetime.now().date().isoformat()
        normalized["total_amount"] = extracted_data.get("total", 0.0)
        normalized["tax_amount"] = extracted_data.get("tax", 0.0)

        items = extracted_data.get("items", [])
        for item in items:
            line_item = {
                "description": item.get("description", ""),
                "quantity": item.get("quantity", 1.0),
                "unit_price": item.get("price", 0.0)
                / max(item.get("quantity", 1.0), 1.0),
                "total": item.get("price", 0.0),
            }
            normalized["line_items"].append(line_item)

    normalized["metadata"]["source_fields"] = extracted_data
    normalized["metadata"]["normalization_version"] = "1.0"

    expense_record = ExpenseRecord(
        expense_id=normalized["expense_id"],
        source_type=normalized["source_type"],
        vendor=normalized["vendor"],
        merchant=normalized["merchant"],
        date=normalized["date"],
        total_amount=normalized["total_amount"],
        tax_amount=normalized["tax_amount"],
        currency=normalized["currency"],
        line_items=[LineItem(**item) for item in normalized["line_items"]],
        metadata=normalized["metadata"],
    )

    return expense_record.dict()
