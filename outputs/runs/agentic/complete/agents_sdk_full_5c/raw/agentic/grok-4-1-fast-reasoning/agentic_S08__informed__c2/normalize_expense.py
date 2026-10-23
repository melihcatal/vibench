import os
import json
from openai import OpenAI
from document_models import NormalizedExpense
from typing import Dict, Any

def normalize_expense(raw_extract: Dict[str, Any], doc_type: str) -> NormalizedExpense:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("Set OPENAI_API_KEY")

    prompt = f"""Normalize this {doc_type} extraction to standard JSON schema. Output ONLY JSON.

Raw: {json.dumps(raw_extract)}

Required JSON:
{{
  "doc_type": "{doc_type}",
  "merchant": "extracted merchant or vendor",
  "date": "date str",
  "total": number,
  "tax": number or null,
  "items": [{{"description": "", "quantity": null, "price": 0}}],
  "avg_confidence": average float
}}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    normalized = json.loads(response.choices[0].message.content or "{}")
    return normalized