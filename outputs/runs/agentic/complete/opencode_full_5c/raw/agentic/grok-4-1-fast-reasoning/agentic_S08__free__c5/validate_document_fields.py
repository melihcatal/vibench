import os
import json
import re
from anthropic import Anthropic
from typing import Dict, Any
from document_models import NormalizedExpense, ValidationResult


def validate_document_fields(normalized: NormalizedExpense) -> ValidationResult:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    prompt = f"""Validate this normalized expense for completeness, accuracy, and reasonableness.
Required: document_type, vendor_merchant, date (YYYY-MM-DD), total >0, line_items not empty.
Date format valid, totals positive, items sum approx total.
Return ONLY JSON: {{"is_valid": boolean, "issues": [string list], "overall_confidence": number 0-1}}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt + f"\n\n{json.dumps(normalized)}"}
        ],
    )
    content = message.content[0].text
    json_str = re.search(r"\{[\\s\\S]*?}", content)
    if json_str:
        result = json.loads(json_str.group())
    else:
        result = {
            "is_valid": False,
            "issues": ["Could not parse validation response"],
            "overall_confidence": 0.0,
        }
    return result
