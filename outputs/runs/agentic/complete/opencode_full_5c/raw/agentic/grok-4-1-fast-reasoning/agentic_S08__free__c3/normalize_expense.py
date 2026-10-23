import os
import json
from openai import OpenAI
from document_models import NormalizedExpense, RawInvoice, RawReceipt
from typing import Union, Dict, Any


def normalize_expense(
    raw_data: Union[Dict[str, Any], RawInvoice, RawReceipt], doc_type: str
) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if hasattr(raw_data, "model_dump"):
        raw_dict = raw_data.model_dump()
    else:
        raw_dict = raw_data

    schema = NormalizedExpense.model_json_schema()
    prompt = f"""Normalize this {doc_type} extraction to the expense schema.

Data:
{json.dumps(raw_dict)}

Strictly return JSON matching this schema:
{json.dumps(schema)}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={
            "type": "json_schema",
            "json_schema": {"name": "expense", "strict": True, "schema": schema},
        },
    )

    normalized = json.loads(response.choices[0].message.content)
    return NormalizedExpense(**normalized)
