import os
import json
from openai import OpenAI
from typing import Dict, Any
from document_models import NormalizedExpense

def normalize_expense(extracted: Dict[str, Any], doc_type: str = 'expense') -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    prompt = f"""Normalize the following {doc_type} extraction into a standard expense schema.

Extracted data:
{json.dumps(extracted, default=str, indent=2)}

Provide JSON object with:
- merchant: str
- date: YYYY-MM-DD
- total: float
- tax: float or null
- items: array of {{description: str, quantity: float or null, unit_price: float or null, total_price: float or null}}

Use the text values from the extraction. Output ONLY valid JSON."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    normalized_json = json.loads(response.choices[0].message.content)
    normalized = NormalizedExpense.model_validate(normalized_json).model_dump()
    return normalized
