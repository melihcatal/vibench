import os
import json
from openai import OpenAI
from typing import Union, Dict, Any
from document_models import InvoiceFields, ReceiptFields, NormalizedExpense


def normalize_expense(
    extracted_fields: Union[InvoiceFields, ReceiptFields],
) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    input_data = json.dumps(extracted_fields, indent=2)
    messages = [
        {
            "role": "system",
            "content": """You normalize extracted invoice or receipt data into a standard expense JSON schema.
            Determine document_type from keys (vendor -> invoice, merchant -> receipt).
            Map merchant to vendor_merchant, items to line_items.
            Compute subtotal if possible: total - tax.
            Output ONLY JSON object with keys: document_type, vendor_merchant, date, total, tax (null if absent), line_items, confidence {}.""",
        },
        {"role": "user", "content": f"Data: {input_data}"},
    ]
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        response_format={"type": "json_object"},
    )
    normalized = json.loads(completion.choices[0].message.content)
    return normalized
