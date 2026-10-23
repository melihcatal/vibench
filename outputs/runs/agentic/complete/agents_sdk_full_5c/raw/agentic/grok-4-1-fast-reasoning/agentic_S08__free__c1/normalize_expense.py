import os
import json
from openai import OpenAI
from document_models import NormalizedExpense
from typing import Dict, Any

def normalize_expense(extracted: Dict[str, Any]) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    type_ = extracted.get('vendor', None) and 'invoice' or 'receipt'
    prompt = f"""Normalize the following {type_} extraction into the standard schema.

Extracted data: {json.dumps(extracted)}

Respond with valid JSON matching this schema:
{NormalizedExpense.model_json_schema()}

Ensure all required fields are filled reasonably."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    data = json.loads(response.choices[0].message.content)
    return NormalizedExpense(**data)
