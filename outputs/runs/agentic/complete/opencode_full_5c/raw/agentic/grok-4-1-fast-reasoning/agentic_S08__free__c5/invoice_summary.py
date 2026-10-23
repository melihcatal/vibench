import os
import json
from openai import OpenAI
from document_models import InvoiceFields
from typing import Dict, Any


def invoice_summary(invoice_fields: InvoiceFields) -> str:
    client = OpenAI(
        api_key=os.getenv("XAI_API_KEY"),
        base_url="https://api.x.ai/v1",
    )
    completion = client.chat.completions.create(
        model="grok-beta",
        messages=[
            {
                "role": "system",
                "content": "Provide a concise 2-3 sentence summary of the invoice including vendor, date, total, and notable line items.",
            },
            {"role": "user", "content": json.dumps(invoice_fields)},
        ],
        max_tokens=200,
    )
    return completion.choices[0].message.content.strip()
