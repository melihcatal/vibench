import os
import json
import uuid
from openai import OpenAI
from dataclasses import asdict
from document_models import NormalizedExpense
from document_client import validate_env
from typing import Dict, Any

validate_env("openai")


def normalize_expense(
    extracted_data: Dict[str, Any], document_type: str
) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = f"""Normalize this {document_type} extraction to standard JSON schema.

Extracted: {json.dumps(extracted_data, default=str, indent=2)}

For invoice: vendor=vendor.value, for receipt: vendor=merchant.value
date: parse to YYYY-MM-DD
total: parse float(total.value)
tax: receipt tax.value float or 0 for invoice
subtotal: total - tax if possible
line_items: list of {{'description': l.description, 'quantity': l.quantity, 'unit_price': l.unit_price, 'total': l.total}} for each line_item
average_confidence: mean of all .confidence fields
Output ONLY JSON object with keys: document_type, vendor, date, subtotal, tax, total, line_items, average_confidence"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    norm_dict = json.loads(response.choices[0].message.content)
    norm_dict["id"] = str(uuid.uuid4())
    norm_dict["document_type"] = document_type
    norm_dict["raw_extraction"] = extracted_data
    return NormalizedExpense(**norm_dict)
