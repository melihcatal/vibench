import os
import json
import anthropic
from typing import Dict, Any


def normalize_expense(extracted: Dict[str, Any], expense_type: str) -> Dict[str, Any]:
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    schema_prompt = (
        """
{
  "type": "%s",
  "vendor_or_merchant": "string",
  "date": "YYYY-MM-DD",
  "total": number,
  "tax": number|null,
  "line_items": [{"description": "string", "quantity": number|null, "unit_price": number|null, "amount": number}]
}
    """
        % expense_type
    )
    user_prompt = f"Normalize this {expense_type} extracted data to standard schema. Parse dates, handle missing. Output ONLY valid JSON object:\n{json.dumps(extracted)}"
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        temperature=0.0,
        system=f"Strictly output JSON matching: {schema_prompt}",
        messages=[{"role": "user", "content": user_prompt}],
    )
    normalized_str = message.content[0].text.strip()
    return json.loads(normalized_str)
