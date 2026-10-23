import json
import re
from typing import Dict, Any
import anthropic
from document_client import get_anthropic_client
from document_models import NormalizedExpense, ValidationResult


def validate_document_fields(normalized: NormalizedExpense) -> ValidationResult:
    client = get_anthropic_client()
    data_str = normalized.model_dump_json()
    prompt = f"""Validate the following normalized expense document.
Check for:
- Required fields: document_type, payee, date, total, line_items (at least one)
- date format plausible (YYYY-MM-DD or MM/DD/YYYY)
- total > 0
- each line_item has description and amount >0
- confidence > 0.5

Output ONLY JSON like: {{"is_valid": true/false, "issues": ["list of issues"], "overall_confidence": 0.92}}

Data: {data_str}"""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    content = message.content[0].text
    json_match = re.search(r"\{.*\}", content, re.DOTALL)
    if json_match:
        val_str = json_match.group()
    else:
        val_str = content
    val_dict = json.loads(val_str)
    return ValidationResult.model_validate(val_dict)
