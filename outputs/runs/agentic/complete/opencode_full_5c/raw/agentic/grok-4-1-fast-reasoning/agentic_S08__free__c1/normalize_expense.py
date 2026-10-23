import os
import json
from openai import OpenAI
from typing import Union
from document_models import InvoiceExtract, ReceiptExtract, NormalizedExpense


def normalize_expense(
    extract: Union[InvoiceExtract, ReceiptExtract],
) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY not set")
    extract_data = extract.model_dump()
    expense_type = "invoice" if isinstance(extract, InvoiceExtract) else "receipt"
    prompt = f"""Normalize this {expense_type} extraction data into the standard NormalizedExpense schema.

Data:
{json.dumps(extract_data, indent=2, default=str)}

Ensure:
- date as YYYY-MM-DD
- amounts as floats
- line_items as list of dicts with description, total_price etc.
- confidence_scores average of main fields
- vendor_or_merchant from vendor or merchant_name.content"""
    schema = {
        "name": "normalized_expense",
        "strict": True,
        "schema": NormalizedExpense.model_json_schema(),
    }
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_schema", "json_schema": schema},
        temperature=0.0,
    )
    normalized_data = json.loads(response.choices[0].message.content)
    return NormalizedExpense.model_validate(normalized_data)
