import os
import json
from document_client import get_openai_client
from document_models import NormalizedExpense, LineItem
from typing import Dict, Any, List

def normalize_expense(raw_expense_data: Dict[str, Any]) -> NormalizedExpense:
    client = get_openai_client()
    
    schema = {
        "type": "object",
        "properties": {
            "vendor_name": {"type": ["string", "null"], "description": "Name of the vendor/merchant"},
            "transaction_date": {"type": ["string", "null"], "format": "date", "description": "Date of the transaction in YYYY-MM-DD format"},
            "total_amount": {"type": ["number", "null"], "description": "Total amount of the expense"},
            "currency": {"type": ["string", "null"], "description": "Currency code (e.g., USD, EUR)"},
            "tax_amount": {"type": ["number", "null"], "description": "Total tax amount"},
            "line_items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "description": {"type": ["string", "null"]},
                        "quantity": {"type": ["number", "null"]},
                        "unit_price": {"type": ["number", "null"]},
                        "total_price": {"type": ["number", "null"]}
                    },
                    "required": []
                },
                "description": "List of line items"
            },
            "document_type": {"type": ["string", "null"], "enum": ["invoice", "receipt"]},
            "confidence_score": {"type": ["number", "null"], "description": "Overall confidence score of extraction (0.0 to 1.0)"},
            "notes": {"type": ["string", "null"], "description": "Any general notes or memo from the document"}
        },
        "required": []
    }

    system_message = f"""You are an expert data normalization system. Your task is to extract and normalize expense-related fields from the provided raw data into a strict JSON schema.
    Ensure dates are in YYYY-MM-DD format. Ensure currency codes are ISO 4217 (e.g., USD, EUR).
    If a field is not present in the raw data, it should be null in the output.
    The output must be a JSON object conforming strictly to the following schema:
    {json.dumps(schema, indent=2)}
    """

    user_message = f"""Raw extracted expense data:
    {json.dumps(raw_expense_data, indent=2)}
    """

    try:
        completion = client.chat.completions.create(
            model=os.environ.get("OPENAI_NORMALIZATION_MODEL", "gpt-4o"),
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ]
        )
        normalized_json = json.loads(completion.choices[0].message.content)
        normalized_json["raw_extraction"] = raw_expense_data

        return NormalizedExpense(**normalized_json)
    except Exception as e:
        return NormalizedExpense(
            vendor_name=raw_expense_data.get("vendor_name") or raw_expense_data.get("merchant_name"),
            transaction_date=raw_expense_data.get("transaction_date"),
            total_amount=raw_expense_data.get("total_amount"),
            currency=raw_expense_data.get("currency"),
            tax_amount=raw_expense_data.get("tax_amount"),
            line_items=[LineItem(**item) for item in raw_expense_data.get("line_items", [])],
            document_type=raw_expense_data.get("document_type"),
            confidence_score=raw_expense_data.get("confidence_score"),
            raw_extraction=raw_expense_data,
            notes=raw_expense_data.get("notes"),
        )