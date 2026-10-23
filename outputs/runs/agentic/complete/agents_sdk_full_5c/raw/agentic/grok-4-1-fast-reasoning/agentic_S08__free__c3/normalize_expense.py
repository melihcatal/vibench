import os
import json
from openai import OpenAI
from typing import Dict, Any
from document_models import NormalizedExpense

def normalize_expense(extracted_fields: Dict[str, Any], expense_type: str) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    schema_prompt = '''
    {
      "expense_type": "invoice" or "receipt",
      "vendor_or_merchant": "str",
      "date": "YYYY-MM-DD",
      "subtotal": "float or null",
      "tax": "float or null",
      "total": "float",
      "line_items": [{"description": "str", "quantity": "float|null", "unit_price": "float", "total_price": "float"}],
      "currency": "USD"
    }
    '''
    prompt = f'''Normalize this {expense_type} extraction into the exact JSON schema. Use extracted values, infer if needed.

Extracted: {json.dumps(extracted_fields)}

Respond with ONLY the JSON object matching the schema:

{schema_prompt}'''

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'},
        temperature=0.1
    )
    normalized = json.loads(response.choices[0].message.content)
    normalized['expense_type'] = expense_type
    return normalized