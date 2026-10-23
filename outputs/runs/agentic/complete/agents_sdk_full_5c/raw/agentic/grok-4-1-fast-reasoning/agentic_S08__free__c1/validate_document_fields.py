import os
import json
import re
from anthropic import Anthropic
from document_models import NormalizedExpense
from typing import Dict, Any

def validate_document_fields(expense: Dict[str, Any]) -> Dict[str, Any]:
    client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    schema_str = json.dumps(NormalizedExpense.model_json_schema(), indent=2)
    prompt = f"""Validate this normalized expense record:

{json.dumps(expense, indent=2)}

1. Check all required fields are present and non-empty.
2. Validate date format (YYYY-MM-DD).
3. Ensure total > 0 and numerical.
4. Assign confidence score (0.0-1.0) to each field based on completeness and reasonableness.
5. Overall valid: true if all required present, confidences > 0.7 avg.

Output ONLY JSON:
{{
  "valid": boolean,
  "issues": ["list of issues"],
  "field_confidences": {{"vendor_or_merchant": 0.95, "date": 0.9, ...}},
  "avg_confidence": 0.92
}}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    content = message.content[0].text
    validation_result = json.loads(re.search(r'\{.*\}', content, re.DOTALL).group())
    return validation_result
