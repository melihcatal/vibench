import os
import json
from anthropic import Anthropic
from document_models import NormalizedExpense, ValidationResult
from typing import Union, Dict, Any


def validate_document_fields(
    expense_data: Union[Dict[str, Any], NormalizedExpense],
) -> ValidationResult:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    if hasattr(expense_data, "model_dump"):
        data = expense_data.model_dump()
    else:
        data = expense_data

    schema = ValidationResult.model_json_schema()
    prompt = f"""Validate expense record. Check completeness, data types, logical consistency (e.g. total = subtotal + tax).

Data: {json.dumps(data, indent=2)}

Output JSON only:
{json.dumps(schema)}"""

    msg = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    validated = json.loads(msg.content[0].text)
    return ValidationResult(**validated)
