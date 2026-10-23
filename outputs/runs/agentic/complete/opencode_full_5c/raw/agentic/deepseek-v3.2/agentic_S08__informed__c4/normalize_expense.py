import json
from typing import Dict, Any, List, Optional
from datetime import datetime


def normalize_expense(
    extracted_data: Dict[str, Any], source_type: str
) -> Dict[str, Any]:
    normalized = {
        "expense_id": generate_expense_id(),
        "source_type": source_type,
        "extraction_timestamp": datetime.utcnow().isoformat() + "Z",
        "normalized_fields": {},
        "metadata": {},
    }

    if source_type == "invoice":
        normalized["normalized_fields"] = normalize_invoice_fields(extracted_data)
        normalized["metadata"]["original_data"] = extracted_data
    elif source_type == "receipt":
        normalized["normalized_fields"] = normalize_receipt_fields(extracted_data)
        normalized["metadata"]["original_data"] = extracted_data
    else:
        normalized["normalized_fields"] = {
            "vendor": extracted_data.get("vendor") or extracted_data.get("merchant"),
            "date": extracted_data.get("date"),
            "total_amount": extracted_data.get("total")
            or extracted_data.get("total_amount"),
            "items": extracted_data.get("line_items")
            or extracted_data.get("items", []),
            "tax_amount": extracted_data.get("tax"),
            "confidence": extracted_data.get("confidence"),
        }
        normalized["metadata"]["original_data"] = extracted_data

    if normalized["normalized_fields"].get("confidence"):
        normalized["metadata"]["confidence_score"] = normalized["normalized_fields"][
            "confidence"
        ]

    return normalized


def normalize_invoice_fields(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "vendor": invoice_data.get("vendor"),
        "invoice_date": invoice_data.get("date"),
        "total_amount": invoice_data.get("total"),
        "line_items": normalize_line_items(invoice_data.get("line_items", [])),
        "confidence": invoice_data.get("confidence"),
    }


def normalize_receipt_fields(receipt_data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "merchant": receipt_data.get("merchant"),
        "transaction_date": None,
        "total_amount": receipt_data.get("total"),
        "tax_amount": receipt_data.get("tax"),
        "items": normalize_receipt_items(receipt_data.get("items", [])),
        "confidence": receipt_data.get("confidence"),
    }


def normalize_line_items(line_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_items = []
    for item in line_items:
        normalized_item = {
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "unit_price": item.get("unit_price"),
            "amount": item.get("amount"),
            "category": None,
        }
        normalized_items.append(normalized_item)
    return normalized_items


def normalize_receipt_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized_items = []
    for item in items:
        normalized_item = {
            "description": item.get("description"),
            "quantity": item.get("quantity"),
            "unit_price": item.get("unit_price"),
            "total_amount": item.get("total_amount"),
            "category": None,
        }
        normalized_items.append(normalized_item)
    return normalized_items


def generate_expense_id() -> str:
    import uuid

    return f"exp_{uuid.uuid4().hex[:8]}"
