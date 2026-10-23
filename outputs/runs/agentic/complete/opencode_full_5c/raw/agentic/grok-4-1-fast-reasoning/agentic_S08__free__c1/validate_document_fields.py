import os
import json
from anthropic import Anthropic
from document_models import NormalizedExpense


def validate_document_fields(normalized: NormalizedExpense) -> dict:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("ANTHROPIC_API_KEY not set")
    prompt = f"""Validate the following normalized expense:

{normalized.model_dump_json(indent=2)}

Perform checks:
1. Required fields present and non-empty
2. date parseable as ISO date
3. total_amount > 0
4. Sum of line_items total_price approx <= total_amount (+10% tolerance)
5. Average confidence > 0.7
6. No suspicious vendor names

Respond with ONLY JSON:
{{
  "valid": true/false,
  "avg_confidence": float,
  "issues": ["list", "of", "issues"]
}}"""
    msg = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        temperature=0.1,
        messages=[{"role": "user", "content": prompt}],
    )
    try:
        result = json.loads(msg.content[0].text)
    except json.JSONDecodeError:
        result = {
            "valid": False,
            "issues": ["Failed to parse validation response"],
            "avg_confidence": 0.0,
        }
    return result
