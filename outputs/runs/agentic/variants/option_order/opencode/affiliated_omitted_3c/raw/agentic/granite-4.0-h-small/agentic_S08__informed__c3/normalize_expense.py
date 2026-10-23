import json
import os


def normalize_expense(raw_data, provider):
    # Provider‑specific mapping to a common schema
    if provider == "textract":
        # Using Amazon Textract AnalyzeExpense output format
        expense = {
            "vendor": raw_data.get("vendor") or "",
            "date": raw_data.get("date") or "",
            "total": raw_data.get("total") or "",
            "line_items": [
                {
                    "vendor": li.get("vendor") or "",
                    "description": li.get("description") or "",
                    "amount": li.get("amount"),
                }
                for li in raw_data.get("line_items", [])
            ],
            "tax": raw_data.get("tax"),
        }
    elif provider == "alibaba":
        # Placeholder mapping for Alibaba Cloud OCR invoice response
        expense = {
            "vendor": raw_data.get("vendor_name") or "",
            "date": raw_data.get("invoice_date") or "",
            "total": raw_data.get("total_amount") or "",
            "line_items": [
                {
                    "vendor": raw_data.get("item_vendor", ""),
                    "description": raw_data.get("item_desc", ""),
                    "amount": raw_data.get("item_amount", ""),
                }
                for _ in []  # Alibaba response format will be filled in later
            ],
            "tax": raw_data.get("tax_amount") or "",
        }
    # Add more provider branches as needed
    else:
        raise ValueError(f"Unknown provider: {provider}")
    return json.dumps(expense, ensure_ascii=False)
