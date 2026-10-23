import openai
import os
import json
from document_models import NormalizedExpense

def normalize_expense(raw_fields: dict) -> dict:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        return {'error': 'Missing OPENAI_API_KEY'}
    client = openai.OpenAI(api_key=api_key)
    schema = NormalizedExpense.model_json_schema()
    prompt = f"""Normalize the raw expense extraction into this JSON schema:

{schema}

Raw data: {json.dumps(raw_fields, indent=2)}

Use vendor or merchant as merchant_name, line_items or items, etc.
Infer missing if possible, but prefer data.
Output ONLY the JSON object matching the schema."""
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        content = response.choices[0].message.content
        normalized_dict = json.loads(content)
        validated = NormalizedExpense(**normalized_dict)
        return validated.model_dump()
    except Exception as e:
        return {'error': str(e)}