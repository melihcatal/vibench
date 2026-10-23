import os
import json
from mistralai.client import MistralClient
from document_models import NormalizedExpense


def validate_document_fields(fields: dict) -> dict:
    try:
        NormalizedExpense(**fields)
    except Exception as e:
        return {"is_valid": False, "issues": [str(e)], "confidence_avg": 0.0}

    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    if not client.api_key:
        raise ValueError("MISTRAL_API_KEY env var required")

    prompt = f"""Validate these normalized expense fields for completeness and consistency:

{json.dumps(fields, default=str)}

Rules:
- Required fields present and non-empty
- Date parseable
- total >= sum(line_items.amounts) + tax
- average confidence > 0.7

Output ONLY JSON: {{"is_valid": true/false, "issues": ["list"], "confidence_avg": float}}"""
    response = client.chat(
        model="mistral-large-latest", messages=[{"role": "user", "content": prompt}]
    )
    result = json.loads(response.choices[0].message.content)
    return result
