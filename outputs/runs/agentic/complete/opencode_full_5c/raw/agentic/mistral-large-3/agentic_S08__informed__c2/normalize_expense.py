from typing import Dict, Any, List
from datetime import datetime
import re


def normalize_expense(extracted_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes extracted expense fields into a standard JSON schema.
    """
    normalized = {
        "vendor": "",
        "merchant": "",
        "date": "",
        "total_amount": 0.0,
        "tax_amount": 0.0,
        "line_items": [],
        "metadata": {
            "source_provider": extracted_data.get("provider", "unknown"),
            "normalization_timestamp": datetime.utcnow().isoformat(),
        },
    }

    # Normalize vendor/merchant
    if "vendor" in extracted_data:
        normalized["vendor"] = extracted_data["vendor"].strip()
    elif "merchant" in extracted_data:
        normalized["merchant"] = extracted_data["merchant"].strip()

    # Normalize date
    date_str = extracted_data.get("date", "")
    if date_str:
        try:
            # Parse common date formats
            if re.match(r"\d{4}-\d{2}-\d{2}", date_str):
                normalized["date"] = date_str
            elif re.match(r"\d{2}/\d{2}/\d{4}", date_str):
                month, day, year = date_str.split("/")
                normalized["date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            elif re.match(r"\d{2}-\d{2}-\d{4}", date_str):
                day, month, year = date_str.split("-")
                normalized["date"] = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
            else:
                normalized["date"] = date_str
        except:
            normalized["date"] = date_str

    # Normalize total and tax
    normalized["total_amount"] = float(extracted_data.get("total", 0.0))
    normalized["tax_amount"] = float(extracted_data.get("tax", 0.0))

    # Normalize line items
    line_items = extracted_data.get("line_items", extracted_data.get("items", []))
    for item in line_items:
        normalized_item = {
            "description": item.get("description", "").strip(),
            "amount": float(item.get("amount", 0.0)),
            "quantity": float(item.get("quantity", 1.0)),
        }
        normalized["line_items"].append(normalized_item)

    return normalized
