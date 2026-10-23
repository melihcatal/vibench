import os
import json
import re
from anthropic import Anthropic
from document_models import ExpenseRecord


def validate_document_fields(extracted_fields: dict) -> dict:
    """
    Validate extracted fields for completeness and confidence using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY required.")

    client = Anthropic(api_key=api_key)

    is_invoice = "vendor" in extracted_fields
    required_fields = ["vendor" if is_invoice else "merchant", "date", "total"] + (
        ["line_items"] if is_invoice else ["items"]
    )
    prompt = f"""Analyze this document extraction:

{json.dumps(extracted_fields, indent=2)}

Determine:
- Presence of required fields: {required_fields}
- Confidence >= 0.8 for vendor/merchant, date, total
- Non-empty values
- Line items present and valid

Output ONLY JSON:
{{
  "valid": boolean,
  "issues": ["list of issues or empty list"],
  "confidence_ok": boolean
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    content = message.content[0].text
    json_str = (
        re.search(r"\{.*\}", content, re.DOTALL).group(0)
        if re.search(r"\{.*\}", content, re.DOTALL)
        else "{}"
    )
    validation = json.loads(json_str)
    return validation
