import json
from typing import Dict, Any
import openai
from document_client import get_openai_client
from document_models import NormalizedExpense, LineItem


def normalize_expense(extracted: Dict[str, Any]) -> NormalizedExpense:
    client = get_openai_client()
    schema_example = {
        "document_type": "invoice",
        "payee": "example vendor",
        "date": "2023-10-01",
        "subtotal": 100.0,
        "tax": 8.0,
        "total": 108.0,
        "line_items": [{"description": "Item1", "amount": 100.0}],
        "confidence": 0.95,
    }
    prompt = f"""Normalize this extracted expense data to a standard JSON schema.
Use 'invoice' or 'receipt' for document_type.
Infer subtotal if possible.
Map fields appropriately.
Respond with ONLY valid JSON:

Data: {json.dumps(extracted)}

Schema example: {json.dumps(schema_example)}"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    normalized_str = response.choices[0].message.content
    normalized_dict = json.loads(normalized_str)
    return NormalizedExpense.model_validate(normalized_dict)
