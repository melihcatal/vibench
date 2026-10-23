import os
import anthropic
import json
from typing import Dict, Any


def validate_document_fields(normalized: Dict[str, Any]) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    prompt = f"""Validate this normalized expense:
{json.dumps(normalized, indent=2)}
Check:
- All required fields present
- Date is valid YYYY-MM-DD
- total_amount > 0
- Average confidence > 0.7
Return JSON only: {{"valid": bool, "issues": [str], "avg_confidence": float}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    )

    validation = json.loads(message.content)
    return validation
