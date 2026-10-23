import os
import openai
import json
from typing import Dict, Any


def normalize_expense(raw_extracted: Dict[str, Any]) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = """You are an expense normalizer. Convert invoice or receipt extracted data to standard schema.
Schema:
{
  "vendor_merchant": "name",
  "date": "YYYY-MM-DD",
  "total_amount": number,
  "tax_amount": number or null,
  "items": [{"description": str, "amount": number}],
  "confidence": {"field": score}
}
Parse and normalize dates, amounts."""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(raw_extracted)},
        ],
        response_format={"type": "json_object"},
    )

    normalized = json.loads(response.choices[0].message.content)
    return normalized
