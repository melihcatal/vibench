import os
import json
from typing import Dict, Any
from openai import OpenAI
from document_models import NormalizedExpense, InvoiceExtract, ReceiptExtract

def normalize_expense(extracted: Dict[str, Any]) -> NormalizedExpense:
    client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
    is_invoice = 'vendor' in extracted
    expense_type = 'invoice' if is_invoice else 'receipt'
    prompt = f"""Normalize this {expense_type} extraction into the standard schema.
Extracted data:
{json.dumps(extracted, indent=2)}

Standard JSON schema:
{{
  "type": "{expense_type}",
  "vendor_or_merchant": "string from vendor or merchant",
  "date": "YYYY-MM-DD format",
  "total": number,
  "tax": number or null,
  "line_items": [
    {{
      "description": "string",
      "quantity": number|null,
      "price": number|null,
      "amount": number
    }}
  ]
}}

Respond with ONLY valid JSON matching this schema exactly."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    normalized_str = response.choices[0].message.content
    normalized = json.loads(normalized_str)
    return NormalizedExpense(**normalized)
