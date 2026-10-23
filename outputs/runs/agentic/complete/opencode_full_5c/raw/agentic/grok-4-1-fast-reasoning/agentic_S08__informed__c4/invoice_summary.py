import os
import json
from anthropic import Anthropic


def invoice_summary(extracted_fields: dict) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    if not client.api_key:
        raise ValueError("ANTHROPIC_API_KEY env var required")

    prompt = f"""Provide a concise 2-3 sentence summary of this invoice:

{json.dumps(extracted_fields, default=str)}"""
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text
