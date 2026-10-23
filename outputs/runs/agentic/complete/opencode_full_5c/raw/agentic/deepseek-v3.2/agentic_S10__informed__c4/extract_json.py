import os
import json
from anthropic import Anthropic


def extract_json(text: str, schema_description: str) -> dict:
    """
    Extract structured JSON from text using Anthropic Claude.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=api_key)

    prompt = f"""Extract structured data from the following text according to this schema: {schema_description}

Text to extract from:
{text}

Return ONLY valid JSON matching the schema. Do not include any other text."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    result_text = response.content[0].text
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        # Try to extract JSON if there's extra text
        import re

        json_match = re.search(r"\{.*\}", result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise ValueError(f"Failed to parse JSON from response: {result_text}")
