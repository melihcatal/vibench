import os
import json
from openai import OpenAI
from document_models import NormalizedExpense, DocumentType


def normalize_expense(raw_fields: dict, document_type: str) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not client.api_key:
        raise ValueError("OPENAI_API_KEY env var required")

    schema = NormalizedExpense.model_json_schema()
    prompt = f"""Normalize these raw {document_type} fields into the following JSON schema exactly.

Raw: {json.dumps(raw_fields)}

Schema:
{schema}

Respond with ONLY valid JSON object matching the schema."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.1,
    )
    normalized = json.loads(response.choices[0].message.content)
    return normalized
