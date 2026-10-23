import os
import json
import openai
from typing import Dict, Any
from document_models import NormalizedExpense

def normalize_expense(raw_extracted: Dict[str, Any]) -> NormalizedExpense:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    system_prompt = """You are an expense data normalizer. Transform the input to a standard JSON schema:
{
  "doc_type": "invoice" | "receipt",
  "entity_name": str,
  "date": "YYYY-MM-DD",
  "tax": float|null,
  "total": float,
  "line_items": [{"description": str, "amount": float}],
  "confidence": {str: float}
}
Use best guess for missing/normalize."""
    user_prompt = f"Raw data: {json.dumps(raw_extracted)}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0.1
    )
    normalized_str = response.choices[0].message.content
    normalized = json.loads(normalized_str)
    return NormalizedExpense(**normalized)
