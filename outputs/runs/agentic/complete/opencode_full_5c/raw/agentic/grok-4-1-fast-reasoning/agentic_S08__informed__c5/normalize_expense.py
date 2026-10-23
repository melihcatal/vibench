import os
import json
from typing import Union
from openai import OpenAI
from document_models import ExtractedInvoice, ExtractedReceipt, NormalizedExpense


def normalize_expense(
    extracted: Union[ExtractedInvoice, ExtractedReceipt],
) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    doc_type = "invoice" if isinstance(extracted, ExtractedInvoice) else "receipt"
    extracted_data = json.dumps(extracted.model_dump(), default=str)
    schema = json.dumps(NormalizedExpense.model_json_schema())
    prompt = f"""Normalize this {doc_type} extraction into standard schema.
Extracted: {extracted_data}

Rules:
- Parse date to YYYY-MM-DD ISO
- Ensure total is number
- vendor_or_merchant from vendor_name or merchant_name
- document_type: '{doc_type}'
- Average confidence values
- Clean line_items

Respond with ONLY JSON matching: {schema}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    data = json.loads(response.choices[0].message.content)
    return NormalizedExpense(**data)
