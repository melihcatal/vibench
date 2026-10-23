import os
import json
from typing import Dict, Any
from mistralai.client import Mistral
from document_models import NormalizedExpense


def validate_document_fields(expense: NormalizedExpense) -> Dict[str, Any]:
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    expense_data = json.dumps(expense.model_dump(), default=str)
    prompt = f"""Validate expense record.
Data: {expense_data}

Checks:
- document_type in ['invoice', 'receipt']
- vendor_or_merchant not empty
- date matches YYYY-MM-DD
- total > 0
- avg(confidence.values()) > 0.7
- line_items not empty

Output ONLY JSON: {{"valid": bool, "issues": ["list"], "avg_confidence": float}}"""
    chat_response = client.chat.complete(
        model="mistral-small-latest", messages=[{"role": "user", "content": prompt}]
    )
    content = chat_response.choices[0].message.content
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"valid": False, "issues": ["Parse error"], "avg_confidence": 0.0}
