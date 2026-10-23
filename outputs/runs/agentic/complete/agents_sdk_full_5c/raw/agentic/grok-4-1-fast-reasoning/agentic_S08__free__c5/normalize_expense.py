import os
import json
from openai import OpenAI
from typing import Dict, Any
from document_models import NormalizedExpense

def normalize_expense(raw_extraction: Dict[str, Any], expense_type: str = 'invoice') -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    schema = NormalizedExpense.model_json_schema()
    prompt = f"""Normalize this {expense_type} extraction into the following JSON schema.

Raw extraction: {json.dumps(raw_extraction, indent=2)}

Provide ONLY the JSON object matching the schema exactly. Generate a unique expense_id like 'exp_' + timestamp."""
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        response_format={'type': 'json_object'},
        temperature=0.1
    )
    normalized_data = json.loads(response.choices[0].message.content)
    normalized_data['type'] = expense_type
    normalized_data['raw_extraction'] = raw_extraction

    return NormalizedExpense(**normalized_data).model_dump()